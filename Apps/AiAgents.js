/**
 * AI Agents for Google Apps Script
 * 
 * 1. Behavioral Economics Story Agent (Google Calendar)
 * 2. News Curator Agent (LINE Notify)
 * 
 * SETUP:
 * 1. File > Project Properties > Script Properties
 *    Add the following properties:
 *    - GEMINI_API_KEY: Your Google Gemini API Key
 *    - LINE_NOTIFY_TOKEN: Your LINE Notify Token
 *    - NEWS_TOPICS: (Optional) Comma separated topics, e.g., "AI,Behavioral Economics,Tech"
 */

// --- Configuration ---
const CONFIG = {
  // Calendar Settings
  CALENDAR_EVENT_TIME: "07:00", // 7:00 AM
  CALENDAR_DURATION_MIN: 15,
  
  // News Settings
  RSS_FEEDS: [
    "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja", // Top Stories Japan
    "https://rss.itmedia.co.jp/rss/2.0/news_bursts.xml", // ITmedia
    // Add more RSS feeds here
  ],
  GEMINI_MODEL: "gemini-1.5-flash"
};

// --- Main Trigger Functions ---

/**
 * Run this function daily (e.g., set trigger for 6:00 AM or 6:30 AM)
 * It will schedule the event for 7:00 AM today.
 */
function runMorningAgent() {
  try {
    const story = generateBehavioralStory();
    if (story) {
      createCalendarEvent(story);
    }
  } catch (e) {
    console.error("Error in Morning Agent:", e);
    // Optional: Send error to LINE/Email
  }
}

/**
 * Run this function periodically (e.g., 8:00 AM and 6:00 PM) to check for news.
 */
function runNewsAgent() {
  try {
    const latestNews = fetchLatestNews();
    if (!latestNews || latestNews.length === 0) {
      console.log("No news found.");
      return;
    }
    
    const curatedNews = curateNewsWithGemini(latestNews);
    
    if (curatedNews) {
      sendLineNotification(curatedNews);
    }
  } catch (e) {
    console.error("Error in News Agent:", e);
  }
}


// --- Agent 1: Behavioral Economics Story ---

function generateBehavioralStory() {
  const prompt = `
  あなたは行動経済学と行動心理学の専門家であり、優れたストーリーテラーです。
  以下の要件に従って、短い学習ストーリーを作成してください。

  1. **テーマ**: 行動経済学または行動心理学の用語を1つランダムに選んでください（例: プロスペクト理論、アンカリング、現状維持バイアス、サンクコスト効果、など）。毎日違うものを選んでください。
  2. **ストーリー**: その理論が日常生活やビジネスでどのように現れるかを示す、短くて面白いストーリー（寓話や具体的なエピソード）を作ってください。
  3. **フォーマット**:
     タイトル: [用語名]
     
     [ストーリー本文 (300文字程度)]
     
     解説: [理論の簡潔な解説 (100文字程度)]
     
     今日のアクション: [読者が今日試せる小さな行動]
  `;

  return callGemini(prompt);
}

function createCalendarEvent(content) {
  // Parse content to get title
  const lines = content.split('\n');
  let title = "【朝の行動経済学】";
  for (const line of lines) {
    if (line.includes("タイトル") || line.includes("Title")) {
      title += " " + line.replace(/タイトル[:：]/, "").trim();
      break;
    }
  }

  const today = new Date();
  // Set time to 7:00 AM today
  const startTime = new Date(today);
  startTime.setHours(7, 0, 0, 0);
  const endTime = new Date(startTime);
  endTime.setMinutes(startTime.getMinutes() + CONFIG.CALENDAR_DURATION_MIN);

  // If script runs after 7AM, schedule for tomorrow? 
  // For now, assume script runs before 7AM. If it's already past 7AM, it creates event in past (which is fine for record) 
  // or simple check:
  if (today.getTime() > startTime.getTime()) {
     // If running after 7AM, maybe schedule for tomorrow?
     // keeping it simple: just create it for "today" even if past, or let user decide trigger time
  }

  const calendar = CalendarApp.getDefaultCalendar();
  const event = calendar.createEvent(title, startTime, endTime, {
    description: content,
    guests: [],
    sendInvites: false
  });
  
  // Add popup 
  event.addPopupReminder(0); // Notification at time of event
  console.log("Created event: " + title);
}


// --- Agent 2: News Curator ---

function fetchLatestNews() {
  let allItems = [];
  
  for (const url of CONFIG.RSS_FEEDS) {
    try {
      const response = UrlFetchApp.fetch(url);
      const xml = XmlService.parse(response.getContentText());
      const root = xml.getRootElement();
      let channel = root.getChild('channel');
      let items = channel.getChildren('item');
      
      // Get top 5 from each feed
      items = items.slice(0, 5);
      
      for (const item of items) {
        allItems.push({
          title: item.getChild('title').getText(),
          link: item.getChild('link').getText(),
          // pubDate: item.getChild('pubDate').getText()
        });
      }
    } catch (e) {
      console.warn("Failed to fetch RSS: " + url, e);
    }
  }
  return allItems;
}

function curateNewsWithGemini(newsItems) {
  const scriptProperties = PropertiesService.getScriptProperties();
  const userTopics = scriptProperties.getProperty("NEWS_TOPICS") || "AI, Technology, Business, Productivity";
  
  const newsListString = newsItems.map((item, index) => `${index + 1}. ${item.title} (${item.link})`).join("\n");
  
  const prompt = `
  あなたはユーザー専用の「ニュース選定エージェント」です。
  ユーザーの関心トピック: ${userTopics}

  以下の最新ニュースリストから、**ユーザーの関心に最も合致する重要なニュースを最大3つ**選んでください。
  関心のあるニュースがない場合は「なし」と答えてください。

  出力形式（LINE通知用なので簡潔に）:
  
  ★ [ニュースタイトル]
  [要約 (1行)]
  [リンク]
  
  (これを最大3件繰り返す)

  ニュースリスト:
  ${newsListString}
  `;

  return callGemini(prompt);
}

function sendLineNotification(message) {
  const token = PropertiesService.getScriptProperties().getProperty("LINE_NOTIFY_TOKEN");
  if (!token) {
    console.error("LINE_NOTIFY_TOKEN is missing");
    return;
  }
  
  if (message.includes("なし") && message.length < 10) {
    console.log("No relevant news to send.");
    return; 
  }

  const options = {
    "method": "post",
    "headers": {
      "Authorization": "Bearer " + token
    },
    "payload": {
      "message": "\n" + message
    }
  };

  UrlFetchApp.fetch("https://notify-api.line.me/api/notify", options);
  console.log("Sent LINE notification");
}


// --- Shared Utilities ---

function callGemini(prompt) {
  const apiKey = PropertiesService.getScriptProperties().getProperty("GEMINI_API_KEY");
  if (!apiKey) {
    throw new Error("GEMINI_API_KEY is not set in Script Properties.");
  }

  const url = `https://generativelanguage.googleapis.com/v1beta/models/${CONFIG.GEMINI_MODEL}:generateContent?key=${apiKey}`;
  
  const payload = {
    "contents": [{
      "parts": [{"text": prompt}]
    }]
  };

  const options = {
    "method": "post",
    "contentType": "application/json",
    "payload": JSON.stringify(payload),
    "muteHttpExceptions": true
  };

  const response = UrlFetchApp.fetch(url, options);
  const json = JSON.parse(response.getContentText());

  if (json.error) {
    throw new Error("Gemini API Error: " + JSON.stringify(json.error));
  }

  return json.candidates[0].content.parts[0].text.trim();
}

/**
 * Setup helper to easily set properties
 * Run this function once manually if you prefer not to use the GUI
 */
function setupKeys() {
  const scriptProperties = PropertiesService.getScriptProperties();
  scriptProperties.setProperties({
    'GEMINI_API_KEY': 'YOUR_GEMINI_KEY_HERE',
    'LINE_NOTIFY_TOKEN': 'YOUR_LINE_TOKEN_HERE',
    'NEWS_TOPICS': 'AI, 行動経済学, スタートアップ'
  });
  console.log("Properties initialized. Please edit them in Project Settings or re-run with actual keys.");
}
