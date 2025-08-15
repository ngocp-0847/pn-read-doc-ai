#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sơ đồ kiến trúc hệ thống Quản lý Vận tải
Dựa trên mô tả từ Mermaid diagram
"""

from diagrams import Diagram
from diagrams.azure.compute import VM
from diagrams.azure.database import DatabaseForMysqlServers
from diagrams.azure.storage import BlobStorage
from diagrams.azure.network import LoadBalancers
from diagrams.azure.ml import CognitiveServices
from diagrams.azure.analytics import SynapseAnalytics

from diagrams.generic.compute import Rack
from diagrams.generic.device import Mobile, Tablet
from diagrams.onprem.client import User, Users
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Postgresql
from diagrams.programming.language import Python
from diagrams.saas.communication import Twilio
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.analytics import Tableau

from diagrams import Cluster

# Tạo sơ đồ với tiếng Việt
with Diagram("Hệ thống Quản lý Vận tải - Kiến trúc Tổng thể", 
             filename="transport_management_architecture_v2", 
             show=False, 
             direction="TB",
             graph_attr={"fontsize": "18", "bgcolor": "white", "nodesep": "1.0", "ranksep": "1.0"}):
    
    # Nhóm người dùng
    with Cluster("Người Dùng"):
        office_staff = User("Nhân viên\nVăn phòng")
        drivers = Mobile("Tài xế\n(Máy tính bảng)")
    
    # Môi trường Azure Cloud
    with Cluster("Môi trường Cloud Azure"):
        # Load balancer
        lb = LoadBalancers("Load Balancer")
        
        # Máy chủ ảo Windows Server
        vm_server = VM("Windows Server\nRAM 32GB")
        
        # Cơ sở dữ liệu
        main_db = DatabaseForMysqlServers("Cơ sở dữ liệu\n< 1TB\n(Thông tin cá nhân)")
        
        # Storage cho file và backup
        storage = BlobStorage("Azure Storage\n(Files & Backup)")
    
    # Hệ thống chính
    with Cluster("Hệ thống Quản lý Vận tải"):
        transport_system = Server("Hệ thống QLVT")
        cache_layer = Redis("Cache Layer\n(Redis)")
    
    # Tích hợp và chức năng nâng cao
    with Cluster("Tích hợp & Chức năng Mới"):
        # Hệ thống kế toán
        bugyo_cloud = Rack("Bugyo Cloud\n(Hệ thống Kế toán)")
        
        # Email service
        email_service = Twilio("Dịch vụ Email\nTự động")
        
        # AI và OCR services
        ai_services = CognitiveServices("AI Dự đoán &\nTối ưu hóa")
        ocr_service = CognitiveServices("OCR\nNhận dạng ký tự")
        
        # Business Intelligence
        bi_tool = SynapseAnalytics("Business Intelligence\nBáo cáo nâng cao")
        
        # Máy in
        printer = Rack("Máy in A4")
    
    # Kết nối người dùng với hệ thống
    office_staff >> lb
    drivers >> lb
    
    # Load balancer phân phối tải
    lb >> vm_server
    
    # Máy chủ ảo chạy hệ thống
    vm_server >> transport_system
    transport_system >> cache_layer
    
    # Kết nối cơ sở dữ liệu
    transport_system >> main_db
    transport_system >> storage
    
    # Tích hợp với các dịch vụ bên ngoài
    transport_system >> bugyo_cloud  # Export CSV định kỳ
    transport_system >> email_service  # Thông báo tiến độ
    transport_system >> printer  # In ấn
    
    # AI và OCR services
    ocr_service >> transport_system  # Xử lý dữ liệu văn bản
    transport_system >> ai_services  # Dữ liệu cho AI và nhận gợi ý
    transport_system >> bi_tool  # Cung cấp dữ liệu cho BI

print("Đã tạo sơ đồ kiến trúc hệ thống thành công!")
print("File output: transport_management_architecture_v2.png")



# Tạo sơ đồ chi tiết các luồng tương tác từ Hệ thống QLVT
with Diagram("Chi tiết Luồng Tương tác - Hệ thống QLVT", 
             filename="transport_detailed_interactions", 
             show=False, 
             direction="LR",
             graph_attr={"fontsize": "16", "bgcolor": "white", "rankdir": "LR", "ranksep": "1.5"}):
    
    # Hệ thống trung tâm
    with Cluster("Hệ thống Quản lý Vận tải (Core)"):
        core_qlvt = Server("Hệ thống QLVT\nCore Engine")
        
        # Các module con trong hệ thống
        with Cluster("Modules Nội bộ"):
            data_processor = Server("Data\nProcessor")
            scheduler = Server("Task\nScheduler")
            api_gateway = Server("API\nGateway")
            file_manager = Server("File\nManager")
    
    # Nhóm các luồng theo hàng để tối ưu layout
    # Hàng 1: CSV Export & Notification
    with Cluster("1. Xuất CSV & Thông báo"):
        with Cluster("CSV Export"):
            csv_scheduler = Server("CSV\nScheduler")
            csv_generator = Server("CSV\nGenerator")
            bugyo_system = Rack("Bugyo\nCloud")
        
        with Cluster("Notification"):
            progress_monitor = Server("Progress\nMonitor")
            notification_engine = Server("Notification\nEngine")
            email_service = Twilio("Email\nService")
    
    # Hàng 2: OCR & AI Processing
    with Cluster("2. Xử lý Thông minh"):
        with Cluster("OCR Processing"):
            document_scanner = Server("Document\nScanner")
            ocr_engine = CognitiveServices("OCR\nEngine")
            text_processor = Server("Text\nProcessor")
        
        with Cluster("AI Integration"):
            ai_service = CognitiveServices("AI\nService")
            prediction_engine = CognitiveServices("Prediction\nEngine")
            optimization_engine = CognitiveServices("Optimization\nEngine")
    
    # Hàng 3: BI & Printing
    with Cluster("3. Báo cáo & In ấn"):
        with Cluster("Business Intelligence"):
            etl_processor = Server("ETL\nProcessor")
            bi_dashboard = SynapseAnalytics("BI\nDashboard")
        
        with Cluster("Printing"):
            print_manager = Server("Print\nManager")
            printer_a4 = Rack("Máy in\nA4")
    
    # Kết nối chính từ Core QLVT
    core_qlvt >> [data_processor, scheduler, api_gateway, file_manager]
    
    # Luồng CSV Export
    scheduler >> csv_scheduler >> csv_generator >> bugyo_system
    
    # Luồng Notification  
    core_qlvt >> progress_monitor >> notification_engine >> email_service
    
    # Luồng OCR (bidirectional)
    document_scanner >> ocr_engine >> text_processor >> core_qlvt
    
    # Luồng AI (bidirectional)
    data_processor >> ai_service
    ai_service >> [prediction_engine, optimization_engine] >> core_qlvt
    
    # Luồng BI
    data_processor >> etl_processor >> bi_dashboard
    
    # Luồng Printing
    core_qlvt >> print_manager >> printer_a4

print("Đã tạo sơ đồ chi tiết luồng tương tác thành công!")
print("File output: transport_detailed_interactions.png")

# Tạo sơ đồ sequence mô tả chi tiết quy trình xử lý
with Diagram("Sequence Flow - Quy trình xử lý chi tiết", 
             filename="transport_sequence_flow", 
             show=False, 
             direction="LR",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    # Các actors chính
    user_office = User("Nhân viên\nVăn phòng")
    user_driver = Mobile("Tài xế")
    
    # Core system với các components
    with Cluster("Hệ thống QLVT"):
        api_gateway = Server("API\nGateway")
        core_engine = Server("Core\nEngine")
        task_scheduler = Server("Task\nScheduler")
        data_processor = Server("Data\nProcessor")
    
    # External services được nhóm theo chức năng
    with Cluster("CSV Export Pipeline"):
        csv_gen = Server("CSV\nGenerator")
        bugyo_cloud = Rack("Bugyo\nCloud")
    
    with Cluster("Notification Pipeline"):
        notif_engine = Server("Notification\nEngine")
        email_svc = Twilio("Email\nService")
    
    with Cluster("OCR Pipeline"):
        ocr_svc = CognitiveServices("OCR\nService")
        text_proc = Server("Text\nProcessor")
    
    with Cluster("AI Pipeline"):
        ai_svc = CognitiveServices("AI\nService")
        prediction = CognitiveServices("Prediction\nEngine")
    
    with Cluster("BI Pipeline"):
        etl_proc = Server("ETL\nProcessor")
        bi_dashboard = SynapseAnalytics("BI\nDashboard")
    
    with Cluster("Print Pipeline"):
        print_mgr = Server("Print\nManager")
        printer = Rack("Máy in\nA4")
    
    # Storage
    database = DatabaseForMysqlServers("Database")
    
    # Sequence flows
    # 1. User input flow
    user_office >> api_gateway
    user_driver >> api_gateway
    api_gateway >> core_engine
    
    # 2. Core processing
    core_engine >> data_processor
    core_engine >> task_scheduler
    data_processor >> database
    
    # 3. Scheduled CSV export
    task_scheduler >> csv_gen
    csv_gen >> bugyo_cloud
    
    # 4. Progress notifications
    core_engine >> notif_engine
    notif_engine >> email_svc
    
    # 5. OCR processing (bidirectional)
    ocr_svc >> text_proc
    text_proc >> core_engine
    
    # 6. AI integration (bidirectional)
    data_processor >> ai_svc
    ai_svc >> prediction
    prediction >> core_engine
    
    # 7. BI reporting
    data_processor >> etl_proc
    etl_proc >> bi_dashboard
    
    # 8. Printing
    core_engine >> print_mgr
    print_mgr >> printer

print("Đã tạo sơ đồ sequence flow thành công!")
print("File output: transport_sequence_flow.png")
