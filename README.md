# smart-mirror

Module.register("youtube_slideshow", {
  defaults: {
    videoIDs: ["dQw4w9WgXcQ", "kJQP7kiw5Fk", "G_wOFcCAvis0"],
    videoDuration: 60 * 1000,
    magicMirrorDuration: 30 * 1000,
    autoplay: false,
    mute: false,
  },

  start: function () {
    this.currentVideoIndex = 0;
    this.isShowingVideo = false;
    this.videoPlayer = null;
    this.videoTimes = new Array(this.config.videoIDs.length).fill(0);

    this.registerKeyEvents();
  },

  registerKeyEvents: function () {
    document.addEventListener("keydown", (event) => {
      if (event.key === "p") {
        this.startVideoPlayback();
      } else if (event.key === "q") {
        this.stopVideoPlayback();
      }
    });
  },

  startVideoPlayback: function () {
    if (!this.isShowingVideo) {
      this.isShowingVideo = true;
      this.scheduleVideoUpdate();
      this.scheduleMagicMirrorUpdate();
      this.updateDom();
    }
  },

  stopVideoPlayback: function () {
    if (this.isShowingVideo) {
      clearInterval(this.videoUpdateInterval);
      clearInterval(this.magicMirrorUpdateInterval);
      this.isShowingVideo = false;
      this.videoPlayer = null; // Clear the video player instance
      this.currentVideoIndex = 0; // Reset to the first video

      this.updateDom(); // This removes the iframe by re-rendering the DOM without it
      this.hide(); // Hide the module
    }
  },

  getDom: function () {
    const wrapper = document.createElement("div");

    if (this.isShowingVideo) {
      const videoID = this.config.videoIDs[this.currentVideoIndex];
      const iframe = document.createElement("iframe");

      iframe.style.position = "absolute";
      iframe.style.top = "0";
      iframe.style.left = "0";
      iframe.style.width = "100vw";
      iframe.style.height = "100vh";
      iframe.src = `https://www.youtube.com/embed/${videoID}?autoplay=1&mute=${this.config.mute ? 1 : 0}&controls=0&rel=0`;
      iframe.frameborder = "0";
      iframe.allow =
        "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      iframe.allowFullscreen = true;

      wrapper.appendChild(iframe);
    }

    return wrapper;
  },

  scheduleVideoUpdate: function () {
    this.videoUpdateInterval = setInterval(() => {
      if (this.videoPlayer) {
        this.videoTimes[this.currentVideoIndex] = this.videoPlayer.getCurrentTime();
      }

      this.currentVideoIndex = (this.currentVideoIndex + 1) % this.config.videoIDs.length;
      this.updateDom();
    }, this.config.videoDuration);
  },

  scheduleMagicMirrorUpdate: function () {
    this.magicMirrorUpdateInterval = setInterval(() => {
      if (this.isShowingVideo) {
        this.isShowingVideo = false;
        this.hide();
      } else {
        this.isShowingVideo = true;
        this.show();

        if (this.videoPlayer) {
          this.videoPlayer.loadVideoById(this.config.videoIDs[this.currentVideoIndex]);
          this.videoPlayer.seekTo(this.videoTimes[this.currentVideoIndex]);
        }

        this.updateDom();
      }
    }, this.config.magicMirrorDuration);
  },
});

