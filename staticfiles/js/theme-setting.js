// =================== Theme Setting js ===================
const lightBtn = document.querySelector("#light-btn");
const darkBtn = document.querySelector("#dark-btn");
const systemBtn = document.querySelector("#system-btn");
const html = document.querySelector("html");
const themeLink = document.querySelector("#change-link");

// تابع برای اعمال تم
function applyTheme(theme) {
  if (theme === "dark") {
    html.className = "dark";
    if (themeLink) themeLink.href = "/static/css/dark.css";
    localStorage.setItem("theme", "dark");
    localStorage.setItem("layoutcss", "/static/css/dark.css");

    // به‌روزرسانی وضعیت دکمه‌ها
    lightBtn.classList.remove("active");
    darkBtn.classList.add("active");
    systemBtn.classList.remove("active");
  }
  else if (theme === "light") {
    html.className = "light";
    if (themeLink) themeLink.href = "/static/css/style.css";
    localStorage.setItem("theme", "light");
    localStorage.setItem("layoutcss", "/static/css/style.css");

    // به‌روزرسانی وضعیت دکمه‌ها
    lightBtn.classList.add("active");
    darkBtn.classList.remove("active");
    systemBtn.classList.remove("active");
  }
  else if (theme === "system") {
    // بررسی تم سیستم
    const systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const systemTheme = systemPrefersDark ? "dark" : "light";

    html.className = systemTheme;
    if (themeLink) themeLink.href = systemPrefersDark ? "/static/css/dark.css" : "/static/css/style.css";
    localStorage.setItem("theme", "system");
    localStorage.setItem("layoutcss", systemPrefersDark ? "/static/css/dark.css" : "/static/css/style.css");

    // به‌روزرسانی وضعیت دکمه‌ها
    lightBtn.classList.remove("active");
    darkBtn.classList.remove("active");
    systemBtn.classList.add("active");
  }
}

// گوش دادن به تغییرات تم سیستم (وقتی کاربر روی حالت system است)
function listenToSystemThemeChange() {
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
    const currentTheme = localStorage.getItem("theme");
    if (currentTheme === "system") {
      const newTheme = e.matches ? "dark" : "light";
      html.className = newTheme;
      if (themeLink) themeLink.href = e.matches ? "/static/css/dark.css" : "/static/css/style.css";
      localStorage.setItem("layoutcss", e.matches ? "/static/css/dark.css" : "/static/css/style.css");
    }
  });
}

// رویدادهای کلیک روی دکمه‌ها
lightBtn?.addEventListener("click", () => {
  applyTheme("light");
});

darkBtn?.addEventListener("click", () => {
  applyTheme("dark");
});

systemBtn?.addEventListener("click", () => {
  applyTheme("system");
});

// بارگذاری تم ذخیره شده در localStorage هنگام لود صفحه
const savedTheme = localStorage.getItem("theme");
if (savedTheme) {
  applyTheme(savedTheme);
} else {
  // اگر تمی ذخیره نشده، از حالت سیستم استفاده کن
  applyTheme("system");
}

// شروع گوش دادن به تغییرات تم سیستم
listenToSystemThemeChange();