const stories = JSON.parse(
    document.getElementById("stories-data").textContent
);

const IMAGE_DURATION = 15000;

let currentIndex = 0;
let progressInterval = null;
let storyTimeout = null;

const imageEl = document.getElementById("imageStory");
const videoEl = document.getElementById("videoStory");
const progressContainer = document.getElementById("progressContainer");
const storyTitle = document.getElementById("storyTitle");

const soundBtn = document.getElementById("soundBtn");

let soundEnabled = false;

// وضعیت اولیه
videoEl.muted = true;
videoEl.volume = 1;

// دکمه صدا
soundBtn.addEventListener("click", async (e) => {

    // جلوگیری از رفتن به استوری بعدی
    e.stopPropagation();

    soundEnabled = !soundEnabled;

    videoEl.muted = !soundEnabled;

    if (soundEnabled) {
        soundBtn.textContent = "🔊 صدا روشن";
    } else {
        soundBtn.textContent = "🔇 پخش صدا";
    }

    if (videoEl.style.display === "block") {
        try {
            await videoEl.play();
        } catch (err) {
            console.log(err);
        }
    }

});

// ساخت نوارهای پیشرفت
stories.forEach(() => {

    const item = document.createElement("div");
    item.className = "progress-item";

    const fill = document.createElement("div");
    fill.className = "progress-fill";

    item.appendChild(fill);
    progressContainer.appendChild(item);

});

function goBack() {

    if (document.referrer) {
        window.location.href = document.referrer;
    } else if (window.history.length > 1) {
        window.history.back();
    } else {
        window.location.href = "/";
    }

}

function updateProgress(index, duration) {

    clearInterval(progressInterval);

    const fills = document.querySelectorAll(".progress-fill");

    fills.forEach((fill, i) => {

        if (i < index) {
            fill.style.width = "100%";
        } else if (i > index) {
            fill.style.width = "0%";
        }

    });

    fills[index].style.width = "0%";

    const startTime = Date.now();

    progressInterval = setInterval(() => {

        const elapsed = Date.now() - startTime;
        const percent = (elapsed / duration) * 100;

        fills[index].style.width = Math.min(percent, 100) + "%";

    }, 30);

}

function showStory(index) {

    clearTimeout(storyTimeout);
    clearInterval(progressInterval);

    if (index >= stories.length) {
        goBack();
        return;
    }

    if (index < 0) {
        index = 0;
    }

    currentIndex = index;

    imageEl.style.display = "none";
    videoEl.style.display = "none";

    videoEl.pause();
    videoEl.currentTime = 0;

    const story = stories[index];

    storyTitle.textContent = story.name || "";

    if (story.type === "image") {

        imageEl.src = story.src;
        imageEl.style.display = "block";

        updateProgress(index, IMAGE_DURATION);

        storyTimeout = setTimeout(() => {

            if (currentIndex === index) {
                showStory(index + 1);
            }

        }, IMAGE_DURATION);

    }

    else if (story.type === "video") {

        videoEl.src = story.src;
        videoEl.style.display = "block";

        // وضعیت صدا حفظ شود
        videoEl.muted = !soundEnabled;
        videoEl.volume = 1;

        videoEl.onloadedmetadata = () => {

            const duration = videoEl.duration * 1000;

            updateProgress(index, duration);

            videoEl.play().catch(err => {
                console.log(err);
            });

        };

        videoEl.onended = () => {

            showStory(currentIndex + 1);

        };

    }

}

// کلیک راست و چپ مثل اینستاگرام
document.querySelector(".story-container")
    .addEventListener("click", function (e) {

        // اگر روی دکمه صدا کلیک شده، هیچ کاری نکن
        if (e.target.closest("#soundBtn")) {
            return;
        }

        const clickX = e.clientX;
        const width = window.innerWidth;

        if (clickX > width / 2) {

            showStory(currentIndex + 1);

        } else {

            if (currentIndex > 0) {
                showStory(currentIndex - 1);
            }

        }

    });

// شروع اولین استوری
showStory(0);