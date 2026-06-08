import cv2
import numpy as np
import os
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MedicineDetector(Node):
    def __init__(self):
        super().__init__('medicine_detector')
        self.dyf_publisher = self.create_publisher(String, 'DYF', 10)
        self.dyfsb_publisher = self.create_publisher(String, 'DYFSB', 10)
        
    def publish_dyf(self):
        msg = String()
        msg.data = "DYF"
        self.dyf_publisher.publish(msg)
        self.get_logger().info('发布话题: DYF')
        
    def publish_dyfsb(self):
        msg = String()
        msg.data = "DYFSB"
        self.dyfsb_publisher.publish(msg)
        self.get_logger().info('发布话题: DYFSB')

def wait_for_camera_device():
    retry_count = 30
    while retry_count > 0:
        if os.path.exists("/dev/video2"):
            print("[状态] 摄像头设备已就绪")
            return
        print("[状态] 等待摄像头设备...")
        time.sleep(3.0)
        retry_count -= 1
    raise RuntimeError("[错误] 等待摄像头设备超时")

class DetectionParams:
    def __init__(self):
        self.white_lower = np.array([0, 0, 200])
        self.white_upper = np.array([180, 30, 255])
        self.min_radius = 15
        self.max_radius = 80
        self.hough_dp = 2
        self.hough_min_dist = 50
        self.area_threshold = 800
        self.circularity_thresh = 0.75
        self.merge_distance = 50

def adaptive_white_detection(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)
    v_lower = max(200, int(avg_brightness * 0.8))
    v_upper = 255
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, (0, 0, v_lower), (180, 30, v_upper))

def enhanced_hough_circle_detection(gray, mask, params):
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    edges = cv2.Canny(blurred, 50, 150)
    masked_edges = cv2.bitwise_and(edges, edges, mask=mask)
    
    circles = cv2.HoughCircles(
        masked_edges, 
        cv2.HOUGH_GRADIENT,
        dp=params.hough_dp,
        minDist=params.hough_min_dist,
        param1=100,
        param2=30,
        minRadius=params.min_radius,
        maxRadius=params.max_radius
    )
    return circles

def verify_circularity(contour):
    perimeter = cv2.arcLength(contour, True)
    area = cv2.contourArea(contour)
    return 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0

def merge_close_detections(detections, merge_distance):
    merged = []
    used = set()
    
    for i, det1 in enumerate(detections):
        if i in used:
            continue
        label1, points1, radius1 = det1
        center1 = np.array(points1) if label1 == "Cap" else np.mean(points1, axis=0)
        
        group = [det1]
        for j, det2 in enumerate(detections[i+1:]):
            label2, points2, radius2 = det2
            center2 = np.array(points2) if label2 == "Cap" else np.mean(points2, axis=0)
            
            distance = np.linalg.norm(center1 - center2)
            if distance < merge_distance:
                group.append(det2)
                used.add(i+1+j)
        
        if len(group) > 1:
            centers = [np.array(p[1]) if p[0] == "Cap" else np.mean(p[1], axis=0) for p in group]
            avg_center = np.mean(centers, axis=0)
            avg_radius = np.mean([p[2] for p in group if p[2] is not None])
            merged.append(("Merged", avg_center, int(avg_radius)))
        else:
            merged.append(det1)
    
    return merged

def detect_bottles(frame, params):
    mask = adaptive_white_detection(frame)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
    refined_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    refined_mask = cv2.morphologyEx(refined_mask, cv2.MORPH_CLOSE, kernel)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = enhanced_hough_circle_detection(gray, refined_mask, params)
    
    contours, _ = cv2.findContours(refined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    detected = []
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            center = (i[0], i[1])
            radius = i[2]
            circle_mask = np.zeros_like(refined_mask)
            cv2.circle(circle_mask, center, radius, 255, -1)
            mean_color = cv2.mean(frame, mask=circle_mask)[:3]
            if np.mean(mean_color) < 200:
                continue
            detected.append(("Cap", center, radius))
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < params.area_threshold:
            continue
            
        circularity = verify_circularity(cnt)
        if circularity < params.circularity_thresh:
            continue
            
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        detected.append(("Body", box, None))
    
    merged_detections = merge_close_detections(detected, params.merge_distance)
    return merged_detections

def visualize(frame, detections):
    for detection in detections:
        label, points, radius = detection
        if label == "Cap":
            x, y = points
            cv2.circle(frame, points, radius, (0, 255, 0), 2)
            cv2.putText(frame, f"({x},{y})", (x-40, y-radius-30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
        elif label == "Body":
            M = cv2.moments(points)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.drawContours(frame, [points], 0, (255, 0, 0), 2)
                cv2.putText(frame, f"({cX},{cY})", (cX-40, cY+30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
        elif label == "Merged":
            x, y = points
            cv2.circle(frame, (int(x), int(y)), radius, (0, 255, 255), 2)
            cv2.putText(frame, f"Merged ({int(x)},{int(y)})", (int(x)-60, int(y)-radius-30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    return frame

def main(args=None):
    rclpy.init(args=args)
    detector_node = MedicineDetector()
    
    params = DetectionParams()
    wait_for_camera_device()
    
    cap = cv2.VideoCapture("/dev/video2")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    cv2.namedWindow("Medicine Detection")
    cv2.createTrackbar("Min Radius", "Medicine Detection", params.min_radius, 100, lambda x: x)
    cv2.createTrackbar("Max Radius", "Medicine Detection", params.max_radius, 200, lambda x: x)
    cv2.createTrackbar("Merge Dist", "Medicine Detection", params.merge_distance, 200, lambda x: x)
    
    # 新增初始化状态变量
    start_time = time.time()
    initialized = False
    last_confirmed_count = 0
    pending_start_time = None
    pending_base_count = 0
    
    try:
        while rclpy.ok():
            ret, frame = cap.read()
            if not ret:
                break
                
            params.min_radius = cv2.getTrackbarPos("Min Radius", "Medicine Detection")
            params.max_radius = cv2.getTrackbarPos("Max Radius", "Medicine Detection")
            params.merge_distance = cv2.getTrackbarPos("Merge Dist", "Medicine Detection")
            
            detections = detect_bottles(frame, params)
            current_count = len(detections)
            
            result_frame = frame.copy()
            cv2.putText(result_frame, f"Count: {current_count}", (20, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # 初始化阶段处理
            current_time = time.time()
            if not initialized:
                elapsed = current_time - start_time
                if elapsed < 3:
                    # 显示初始化倒计时
                    cv2.putText(result_frame, 
                               f"Initializing: {3 - int(elapsed)}s", 
                               (20, 80),
                               cv2.FONT_HERSHEY_SIMPLEX, 
                               0.8, (0, 0, 255), 2)
                    result_frame = visualize(result_frame, detections)
                    cv2.imshow("Medicine Detection", result_frame)
                    cv2.waitKey(1)
                    continue  # 跳过状态处理
                else:
                    # 初始化基准数量
                    last_confirmed_count = current_count
                    initialized = True
                    print(f"[状态] 初始基准数量设置为: {last_confirmed_count}")

            # 状态机逻辑
            if pending_start_time is None:
                if current_count < last_confirmed_count:
                    pending_start_time = time.time()
                    pending_base_count = current_count
                    print(f"[状态] 数量减少至 {current_count}，进入5秒确认期")
                else:
                    last_confirmed_count = current_count
            else:
                elapsed = time.time() - pending_start_time
                if elapsed >= 5:
                    if current_count <= pending_base_count:
                        print("[动作] 发布话题：DYF（药瓶已拿走）")
                        detector_node.publish_dyf()
                        cap.release()
                        cv2.destroyAllWindows()
                        detector_node.destroy_node()
                        rclpy.shutdown()
                        return
                    else:
                        print("[动作] 发布话题：DYFSB（药瓶未被拿走）")
                        detector_node.publish_dyfsb()
                    last_confirmed_count = current_count
                    pending_start_time = None
                else:
                    cv2.putText(result_frame, 
                               f"Confirming: {5-int(elapsed)}s", 
                               (20, 80),
                               cv2.FONT_HERSHEY_SIMPLEX, 
                               0.8, (0, 0, 255), 2)
            
            result_frame = visualize(result_frame, detections)
            cv2.imshow("Medicine Detection", result_frame)
            
            if cv2.waitKey(1) == 27:
                break
            
            rclpy.spin_once(detector_node, timeout_sec=0.001)
            
    except Exception as e:
        print(f"[错误] {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        detector_node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()