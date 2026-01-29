function formatToIST(utcDate) {
  return new Date(utcDate).toLocaleString("en-IN", {
    timeZone: "Asia/Kolkata",
    day: "2-digit",
    month: "long",
    year: "numeric",
    hour: "numeric",      // 👈 IMPORTANT (not 2-digit)
    minute: "2-digit",
    hour12: true          // 👈 forces 12-hour format
  }) + " IST";
}


async function loadEvents() {
  const response = await fetch("/events");
  const events = await response.json();

  const list = document.getElementById("event-list");
  list.innerHTML = "";

  events.forEach(event => {
    let message = "";

    if (event.action === "PUSH") {
      message = `${event.author} pushed to ${event.to_branch} on ${formatToIST(event.created_at)}`;
    } 
    else if (event.action === "PULL_REQUEST") {
      message = `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${formatToIST(event.created_at)}`;
    } 
    else if (event.action === "MERGE") {
      message = `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${formatToIST(event.created_at)}`;
    }

    const li = document.createElement("li");
    li.textContent = message;
    list.appendChild(li);
  });
}

loadEvents();
setInterval(loadEvents, 15000);
