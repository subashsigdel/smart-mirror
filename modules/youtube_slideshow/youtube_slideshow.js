Module.register("youtube_slideshow", {
  defaults: {
    videoIDs: ["MQ_p1qmrxPI","_OjRClPzU6Y", "CE56q1EpArQ&t=110s", "b2l5uNkIKRM"],
    videoDuration: 2 * 60 * 1000,
    magicMirrorDuration: 30 * 1000,
    autoplay: false,
    mute: false,
  },

  start: function () {
    this.currentVideoIndex = 0;
    this.isShowingVideo = false;
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
      this.updateDom(); // Render the iframe
      this.scheduleVideoUpdate();
      this.scheduleMagicMirrorUpdate();
    }
  },

  stopVideoPlayback: function () {
    if (this.isShowingVideo) {
      clearInterval(this.videoUpdateInterval);
      clearInterval(this.magicMirrorUpdateInterval);
      this.isShowingVideo = false;
      
      this.currentVideoIndex = 0; // Reset to the first video
      this.updateDom(); // Clear the iframe from the DOM
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
      iframe.frameBorder = "0";
      iframe.allow = "autoplay; encrypted-media";
      iframe.allowFullscreen = true;

      wrapper.appendChild(iframe);
    }

    return wrapper;
  },

  scheduleVideoUpdate: function () {
    clearInterval(this.videoUpdateInterval); // Clear any existing interval
    this.videoUpdateInterval = setInterval(() => {
      this.currentVideoIndex = (this.currentVideoIndex + 1) % this.config.videoIDs.length;
      this.updateDom(); // Update DOM to show the next video
    }, this.config.videoDuration);
  },

  scheduleMagicMirrorUpdate: function () {
    clearInterval(this.magicMirrorUpdateInterval); // Clear any existing interval
    this.magicMirrorUpdateInterval = setInterval(() => {
      if (this.isShowingVideo) {
        this.isShowingVideo = false;
        this.updateDom(); // Clear the iframe from the DOM
      } else {
        this.isShowingVideo = true;
        this.updateDom(); // Update DOM to recreate iframe
      }
    }, this.config.magicMirrorDuration);
  },
});

