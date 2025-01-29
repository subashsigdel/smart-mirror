from runner.runner import MayaApp

if __name__ == "__main__":
    app = MayaApp("modules/MMM-FaceRecognition/ObjectDetection/yolov8n.pt")
    app.run()

