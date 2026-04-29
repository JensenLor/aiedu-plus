const DATA_FILES = {
    categories: "data/categories.csv",
    resources: "data/resources.csv"
};

const state = {
    categories: [],
    resources: [],
    activeCategory: "all"
};

const elements = {};

document.addEventListener("DOMContentLoaded", () => {
    elements.nav = document.getElementById("categoryNav");
    elements.grid = document.getElementById("resourceGrid");
    elements.status = document.getElementById("resourceStatus");
    elements.empty = document.getElementById("emptyState");
    elements.downloadSection = document.getElementById("downloadSection");
    elements.downloadGrid = document.getElementById("downloadGrid");

    initializePage();
});

async function initializePage() {
    try {
        setStatus("正在读取资料数据...");

        const [categoryText, resourceText] = await Promise.all([
            fetchText(DATA_FILES.categories),
            fetchText(DATA_FILES.resources)
        ]);

        state.categories = parseCSV(categoryText)
            .map(row => {
                const categoryId = getCell(row, ["id", "分类ID"]);
                return {
                    id: categoryId,
                    name: getCell(row, ["name", "分类名称"]),
                    icon: sanitizeIcon(getCell(row, ["icon", "图标"]), getDefaultCategoryIcon(categoryId)),
                    description: getCell(row, ["description", "分类说明", "说明"]) || "",
                    sort: toNumber(getCell(row, ["sort", "排序"]), 9999),
                    enabled: toBoolean(getCell(row, ["enabled", "启用"]))
                };
            })
            .filter(item => item.id && item.name && item.enabled)
            .sort((a, b) => a.sort - b.sort);

        const categoryMap = new Map(state.categories.map(item => [item.id, item]));

        state.resources = parseCSV(resourceText)
            .map(row => {
                const categoryId = getCell(row, ["category_id", "分类ID"]);
                const categoryIcon = categoryMap.get(categoryId)?.icon || getDefaultCategoryIcon(categoryId);
                const downloadUrl = getCell(row, ["download_url", "下载链接", "downloadLink"]);
                return {
                    id: getCell(row, ["id", "资源ID"]),
                    categoryId,
                    title: getCell(row, ["title", "标题"]),
                    url: getCell(row, ["url", "网址", "链接"]),
                    description: getCell(row, ["description", "一句话简介", "简介"]) || "",
                    details: getCell(row, ["details", "详细说明"]) || getCell(row, ["description", "一句话简介", "简介"]) || "",
                    tags: splitList(getCell(row, ["tags", "标签"])),
                    meta: splitList(getCell(row, ["meta", "补充信息", "备注"])),
                    icon: getResourceIcon(getCell(row, ["icon", "图标"]), getCell(row, ["url", "网址", "链接"]), categoryIcon),
                    badge: getCell(row, ["badge", "角标"]) || "",
                    sort: toNumber(getCell(row, ["sort", "排序"]), 9999),
                    enabled: toBoolean(getCell(row, ["enabled", "启用"])),
                    categoryName: categoryMap.get(categoryId)?.name || "未分类",
                    categoryIcon,
                    version: getCell(row, ["version", "版本", "版本号"]) || "",
                    fileSize: getCell(row, ["file_size", "文件大小", "大小"]) || "",
                    downloadUrl
                };
            })
            .filter(item => item.id && item.title && item.enabled)
            .sort((a, b) => a.sort - b.sort || a.title.localeCompare(b.title, "zh-CN"));

        renderNav();
        setActiveCategory(resolveInitialCategory(), false);

        window.addEventListener("hashchange", () => {
            setActiveCategory(resolveInitialCategory(), false);
        });

        hideStatus();
    } catch (error) {
        console.error(error);
        showError("资料数据读取失败，请确认通过本地服务器或线上地址访问页面，并检查 CSV 文件格式是否正确。");
    }
}

async function fetchText(url) {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) {
        throw new Error(`Failed to fetch ${url}: ${response.status}`);
    }

    const buffer = await response.arrayBuffer();
    return decodeCSVText(buffer);
}

function decodeCSVText(buffer) {
    const bytes = new Uint8Array(buffer);
    if (!bytes.length) {
        return "";
    }

    if (bytes.length >= 3 && bytes[0] === 0xEF && bytes[1] === 0xBB && bytes[2] === 0xBF) {
        return new TextDecoder("utf-8").decode(bytes);
    }

    try {
        return new TextDecoder("utf-8", { fatal: true }).decode(bytes);
    } catch (error) {
        return new TextDecoder("gb18030").decode(bytes);
    }
}

function parseCSV(text) {
    const rows = [];
    let row = [];
    let cell = "";
    let inQuotes = false;

    for (let i = 0; i < text.length; i += 1) {
        const char = text[i];
        const next = text[i + 1];

        if (inQuotes) {
            if (char === '"' && next === '"') {
                cell += '"';
                i += 1;
            } else if (char === '"') {
                inQuotes = false;
            } else {
                cell += char;
            }
        } else if (char === '"') {
            inQuotes = true;
        } else if (char === ',') {
            row.push(cell);
            cell = "";
        } else if (char === '\n') {
            row.push(cell);
            if (row.some(value => value.trim() !== "")) {
                rows.push(row);
            }
            row = [];
            cell = "";
        } else if (char !== '\r') {
            cell += char;
        }
    }

    row.push(cell);
    if (row.some(value => value.trim() !== "")) {
        rows.push(row);
    }

    if (rows.length === 0) {
        return [];
    }

    const headers = rows.shift().map((header) => header.replace(/^\uFEFF/, "").trim());

    return rows.map((cells) => {
        const item = {};
        headers.forEach((header, index) => {
            item[header] = (cells[index] || "").trim();
        });
        return item;
    });
}

function getCell(row, keys) {
    for (const key of keys) {
        if (Object.prototype.hasOwnProperty.call(row, key)) {
            const value = row[key];
            if (value !== undefined && value !== null && String(value).trim() !== "") {
                return String(value).trim();
            }
        }
    }

    for (const key of keys) {
        if (Object.prototype.hasOwnProperty.call(row, key)) {
            const value = row[key];
            return value === undefined || value === null ? "" : String(value).trim();
        }
    }

    return "";
}

function getDefaultCategoryIcon(categoryId) {
    const iconMap = {
        ai: "🤖",
        programming: "💻",
        hardware: "🔧",
        "3d": "🖨️",
        robotics: "🤖",
        games: "🎮",
        math: "📐",
        tools: "🧰",
        competition: "🏆"
    };

    return iconMap[categoryId] || "📚";
}

function sanitizeIcon(value, fallback = "📚") {
    const icon = normalizeIconValue(value);
    return icon || fallback;
}

function normalizeIconValue(value) {
    const icon = String(value || "").trim();
    if (!icon || /^[?？]+$/.test(icon)) {
        return "";
    }

    return icon;
}

function getResourceIcon(iconValue, url, fallback = "📚") {
    const explicitIcon = normalizeIconValue(iconValue);
    if (explicitIcon) {
        return explicitIcon;
    }

    return getSiteIconUrl(url) || fallback;
}

function getSiteIconUrl(url) {
    if (!url) {
        return "";
    }

    try {
        const parsed = new URL(url);
        const hostname = parsed.hostname.toLowerCase();
        const iconOverrides = {
            "chat.deepseek.com": "https://www.deepseek.com/favicon.ico",
            "www.deepseek.com": "https://www.deepseek.com/favicon.ico",
            "deepseek.com": "https://www.deepseek.com/favicon.ico",
            "www.doubao.com": "https://lf-flow-web-cdn.doubao.com/obj/flow-doubao/favicon/128x128.png",
            "doubao.com": "https://lf-flow-web-cdn.doubao.com/obj/flow-doubao/favicon/128x128.png",
            "www.kimi.com": "https://statics.moonshot.cn/kimi-web-seo/favicon.ico",
            "kimi.com": "https://statics.moonshot.cn/kimi-web-seo/favicon.ico",
            "kimi.moonshot.cn": "https://statics.moonshot.cn/kimi-web-seo/favicon.ico",
            "www.qianwen.com": "https://img.alicdn.com/imgextra/i4/O1CN01uar8u91DHWktnF2fl_!!6000000000191-2-tps-110-110.png",
            "qianwen.com": "https://img.alicdn.com/imgextra/i4/O1CN01uar8u91DHWktnF2fl_!!6000000000191-2-tps-110-110.png",
            "3d.hunyuan.tencent.com": "https://cdn-3d-prod.hunyuan.tencent.com/public/static/favicon/favicon-32x32.png"
        };

        return iconOverrides[hostname] || `${parsed.origin}/favicon.ico`;
    } catch (error) {
        return "";
    }
}

function isImageIcon(value) {
    return /^(https?:)?\/\//i.test(String(value || "").trim()) || /^data:image\//i.test(String(value || "").trim());
}

function toAbsoluteIconUrl(value) {
    const icon = String(value || "").trim();
    if (icon.startsWith("//")) {
        return `https:${icon}`;
    }

    return icon;
}

function renderNav() {
    const navItems = [
        { id: "all", name: "全部资源", icon: "📖" },
        ...state.categories
    ];

    elements.nav.innerHTML = navItems.map((item) => `
        <li>
            <a href="#${escapeAttr(item.id)}" data-category="${escapeAttr(item.id)}">
                ${escapeHtml(item.icon)} ${escapeHtml(item.name)}
            </a>
        </li>
    `).join("");

    elements.nav.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", (event) => {
            event.preventDefault();
            const categoryId = link.dataset.category || "all";
            setActiveCategory(categoryId);
        });
    });
}

function setActiveCategory(categoryId, updateHash = true) {
    const validIds = new Set(["all", ...state.categories.map(item => item.id)]);
    const nextCategory = validIds.has(categoryId) ? categoryId : "all";

    state.activeCategory = nextCategory;

    elements.nav.querySelectorAll("a").forEach((link) => {
        link.classList.toggle("active", link.dataset.category === nextCategory);
    });

    if (updateHash) {
        const nextHash = `#${nextCategory}`;
        if (window.location.hash !== nextHash) {
            history.replaceState(null, "", nextHash);
        }
    }

    renderResources();
}

function renderResources() {
    const filteredResources = state.activeCategory === "all"
        ? state.resources
        : state.resources.filter((item) => item.categoryId === state.activeCategory);

    if (filteredResources.length === 0) {
        elements.grid.innerHTML = "";
        elements.empty.hidden = false;
        return;
    }

    elements.empty.hidden = true;
    elements.grid.innerHTML = filteredResources.map(renderCard).join("");
    attachCardIconFallbacks();
}

function renderCard(item) {
    const hasDownload = !!item.downloadUrl;
    const content = `
        ${item.badge ? `<span class="card-badge">${escapeHtml(item.badge)}</span>` : ""}
        ${renderCardIcon(item.icon, item.categoryIcon)}
        <h3 class="card-title">${escapeHtml(item.title)}</h3>
        <p class="card-description">${escapeHtml(item.description)}</p>
        ${hasDownload ? `
        <div class="card-download-meta">
            ${item.version ? `<span class="meta-tag">📦 ${escapeHtml(item.version)}</span>` : ""}
            ${item.fileSize ? `<span class="meta-tag">💾 ${escapeHtml(item.fileSize)}</span>` : ""}
            <button class="card-download-btn" onclick="openDownloadModal(${JSON.stringify(item).replace(/"/g, '&quot;')})">
                ⬇️ 立即下载
            </button>
        </div>
        ` : ""}
    `;

    if (hasDownload) {
        return `
            <article class="resource-card" data-resource-id="${escapeAttr(item.id)}">
                ${content}
            </article>
        `;
    }

    if (item.url) {
        return `
            <a class="resource-card" data-resource-id="${escapeAttr(item.id)}" href="${escapeAttr(item.url)}" target="_blank" rel="noopener noreferrer">
                ${content}
            </a>
        `;
    }

    return `
        <article class="resource-card resource-card-static" data-resource-id="${escapeAttr(item.id)}">
            ${content}
        </article>
    `;
}

function renderCardIcon(icon, fallbackIcon = "📚") {
    const safeFallback = sanitizeIcon(fallbackIcon, "📚");

    if (isImageIcon(icon)) {
        return `
            <div class="card-icon card-icon-media" aria-hidden="true">
                <img class="card-icon-image" src="${escapeAttr(toAbsoluteIconUrl(icon))}" alt="" loading="lazy" referrerpolicy="no-referrer">
                <span class="card-icon-fallback">${escapeHtml(safeFallback)}</span>
            </div>
        `;
    }

    return `<div class="card-icon" aria-hidden="true">${escapeHtml(icon || safeFallback)}</div>`;
}

function attachCardIconFallbacks() {
    elements.grid.querySelectorAll(".card-icon-image").forEach((image) => {
        image.addEventListener("error", () => {
            image.closest(".card-icon")?.classList.add("icon-failed");
        }, { once: true });
    });
}

function resolveInitialCategory() {
    const hash = decodeURIComponent(window.location.hash.replace(/^#/, "").trim());
    return hash || "all";
}

function splitList(value) {
    if (!value) {
        return [];
    }

    if (value.includes("|")) {
        return value.split("|").map(item => item.trim()).filter(Boolean);
    }

    if (value.includes("｜")) {
        return value.split("｜").map(item => item.trim()).filter(Boolean);
    }

    if (value.includes("，")) {
        return value.split("，").map(item => item.trim()).filter(Boolean);
    }

    if (value.includes(",")) {
        return value.split(",").map(item => item.trim()).filter(Boolean);
    }

    return [value.trim()].filter(Boolean);
}

function toNumber(value, fallback) {
    const result = Number(value);
    return Number.isFinite(result) ? result : fallback;
}

function toBoolean(value) {
    if (value === undefined || value === null || value === "") {
        return true;
    }

    return !["0", "false", "False", "FALSE", "no", "No", "NO"].includes(String(value).trim());
}

function getDomainLabel(url) {
    if (!url) {
        return "";
    }

    try {
        const parsed = new URL(url);
        return parsed.hostname.replace(/^www\./, "");
    } catch (error) {
        return "";
    }
}

function setStatus(message) {
    elements.status.hidden = false;
    elements.status.className = "status-box";
    elements.status.textContent = message;
}

function hideStatus() {
    elements.status.hidden = true;
    elements.status.textContent = "";
}

function showError(message) {
    elements.status.hidden = false;
    elements.status.className = "status-box error";
    elements.status.textContent = message;
    elements.grid.innerHTML = "";
    elements.empty.hidden = true;
}

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\"/g, "&quot;")
        .replace(/'/g, "&#39;");
}

function escapeAttr(value) {
    return escapeHtml(value).replace(/`/g, "&#96;");
}

let currentDownloadItem = null;
let downloadInterval = null;

function openDownloadModal(item) {
    currentDownloadItem = item;
    
    document.getElementById("confirmIcon").textContent = item.icon || item.categoryIcon || "⚙️";
    document.getElementById("confirmName").textContent = item.title;
    document.getElementById("confirmDesc").textContent = item.description;
    document.getElementById("confirmVersion").textContent = item.version || "未知版本";
    document.getElementById("confirmSize").textContent = item.fileSize || "未知大小";
    
    document.getElementById("confirmContent").hidden = false;
    document.getElementById("progressContent").hidden = true;
    document.getElementById("successContent").hidden = true;
    
    document.getElementById("downloadModal").hidden = false;
    document.body.style.overflow = "hidden";
}

function closeDownloadModal() {
    document.getElementById("downloadModal").hidden = true;
    document.body.style.overflow = "";
    
    if (downloadInterval) {
        clearInterval(downloadInterval);
        downloadInterval = null;
    }
    
    document.getElementById("progressFill").style.width = "0%";
    document.getElementById("progressText").textContent = "0%";
    
    currentDownloadItem = null;
}

function startDownload() {
    if (!currentDownloadItem) return;
    
    document.getElementById("confirmContent").hidden = true;
    document.getElementById("progressContent").hidden = false;
    document.getElementById("successContent").hidden = true;
    
    let progress = 0;
    downloadInterval = setInterval(() => {
        progress += Math.random() * 15 + 5;
        if (progress >= 100) {
            progress = 100;
            clearInterval(downloadInterval);
            downloadInterval = null;
            
            setTimeout(() => {
                simulateDownloadComplete();
            }, 300);
        }
        
        document.getElementById("progressFill").style.width = `${progress}%`;
        document.getElementById("progressText").textContent = `${Math.round(progress)}%`;
    }, 200);
}

function simulateDownloadComplete() {
    if (!currentDownloadItem) return;
    
    document.getElementById("progressContent").hidden = true;
    document.getElementById("successContent").hidden = false;
    
    const downloadLink = document.createElement("a");
    downloadLink.href = currentDownloadItem.downloadUrl;
    downloadLink.download = currentDownloadItem.title;
    downloadLink.target = "_blank";
    downloadLink.rel = "noopener noreferrer";
    
    setTimeout(() => {
        downloadLink.click();
    }, 500);
}

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !document.getElementById("downloadModal").hidden) {
        closeDownloadModal();
    }
});
