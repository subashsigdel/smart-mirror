const NodeHelper = require("node_helper");
const { exec } = require("child_process");

module.exports = NodeHelper.create({
  start: function() {
    console.log("Node Helper for MMM-FaceRecognition started.");
  },

  socketNotificationReceived: function(notification, payload) {
    if (notification === 'RUN_SCRIPT') {
      this.runPythonScript();
    }
    if (notification === 'RUN_SCRIPT2') {
      this.runPythonScript2();
    }
    if (notification === 'RUN_SCRIPT3') {
      this.runPythonScript3();
    }
    if (notification === 'RUN_SCRIPT4') {
      this.runPythonScript4();
    }
    
  },
  

  runPythonScript: function() {
    const command = "python3 modules/MMM-FaceRecognition/face_detect.py"; // Replace with your script path

    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing script: ${error}`);
        return;
      }

      console.log(`Script output: ${stdout}`);
      if (stderr) {
        console.error(`Script error output: ${stderr}`);
      }

      // Notify the module that the script has completed
      this.sendSocketNotification('SCRIPT_COMPLETED');
    });
  },
  runPythonScript2: function() {
    const command = "python3 /home/hitech/MagicMirrornew/modules/MMM-FaceRecognition/ObjectDetection/main.py"; // Replace with your script path

    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing script: ${error}`);
        return;
      }

      console.log(`Script output: ${stdout}`);
      if (stderr) {
        console.error(`Script error output: ${stderr}`);
      }

      // Notify the module that the script has completed
      this.sendSocketNotification('SCRIPT_COMPLETED');
    });
  },
  runPythonScript4: function() {
    const command = "python3 /home/hitech/MagicMirrornew/smolvlm-VisionLanguageModel/VisionLanguageModel.py"; // Replace with your script path

    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing script: ${error}`);
        return;
      }

      console.log(`Script output: ${stdout}`);
      if (stderr) {
        console.error(`Script error output: ${stderr}`);
      }

      // Notify the module that the script has completed
      this.sendSocketNotification('SCRIPT_COMPLETED');
    });
  },
  runPythonScript3: function() {
    const command = "python3 modules/youtube_slideshow/news_speak.py"; // Replace with your script path

    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing script: ${error}`);
        return;
      }

      console.log(`Script output: ${stdout}`);
      if (stderr) {
        console.error(`Script error output: ${stderr}`);
      }

      // Notify the module that the script has completed
      this.sendSocketNotification('SCRIPT_COMPLETED');
    });
  },
});
