function setupDailyReminders() {
    // --- CONFIGURATION ---
    const CALENDAR_NAME = ""; // Leave empty to use default calendar, or specify name
    const EVENTS = [
        { title: "🌅 Self-Analysis: Morning Reflection", time: "08:00" },
        { title: "☀️ Self-Analysis: Lunchtime Check-in", time: "12:00" },
        { title: "🌙 Self-Analysis: Daily Review", time: "21:00" }
    ];
    // ---------------------

    const calendar = CALENDAR_NAME ? CalendarApp.getCalendarsByName(CALENDAR_NAME)[0] : CalendarApp.getDefaultCalendar();

    if (!calendar) {
        Logger.log("Error: Calendar not found.");
        return;
    }

    // 1. Clear existing triggers to avoid duplicates
    const triggers = ScriptApp.getProjectTriggers();
    for (const trigger of triggers) {
        if (trigger.getHandlerFunction() === "createDailyEvents") {
            ScriptApp.deleteTrigger(trigger);
        }
    }

    // 2. Set up a new trigger to run every day at 1 AM
    // This function 'createDailyEvents' will be called once a day to create that day's events
    ScriptApp.newTrigger("createDailyEvents")
        .timeBased()
        .everyDays(1)
        .atHour(1) // Run at 1 AM
        .create();

    Logger.log("✅ Setup Complete. Reminders will be created daily at 1 AM.");

    // Optional: Run once now to populate today's remaining events?
    // enhance: For simplicity, let's just create tomorrow's events or leave it to the trigger.
    // Actually, let's create *today's* events right now for immediate feedback.
    createDailyEvents();
}

function createDailyEvents() {
    const CALENDAR_NAME = ""; // Same config
    const EVENTS = [
        { title: "🌅 Self-Analysis: Morning Reflection", time: "08:00" },
        { title: "☀️ Self-Analysis: Lunchtime Check-in", time: "12:00" },
        { title: "🌙 Self-Analysis: Daily Review", time: "21:00" }
    ];

    const calendar = CALENDAR_NAME ? CalendarApp.getCalendarsByName(CALENDAR_NAME)[0] : CalendarApp.getDefaultCalendar();
    const today = new Date();

    EVENTS.forEach(event => {
        const [hour, minute] = event.time.split(":");

        const startTime = new Date(today);
        startTime.setHours(parseInt(hour), parseInt(minute), 0);

        const endTime = new Date(startTime);
        endTime.setMinutes(endTime.getMinutes() + 15); // 15 min duration

        // Only create if time is in the future (or if running via trigger at 1 AM, all are in future)
        // For manual 'setupDailyReminders' run, we might want to skip passed times, but duplicating for today is acceptible testing.

        calendar.createEvent(event.title, startTime, endTime, {
            description: "Time to open 'Self_Analysis_Work' and write your thoughts!\nUse 'Run_Strategist_Agent' if you are stuck."
        });
    });

    Logger.log(`Created ${EVENTS.length} events for ${today.toDateString()}`);
}
