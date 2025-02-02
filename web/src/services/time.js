export const dateToString = (d) => {
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0"); // Months are zero-based
  const dd = String(d.getDate()).padStart(2, "0");
  const HH = String(d.getHours()).padStart(2, "0");
  const MM = String(d.getMinutes()).padStart(2, "0");

  return `${yyyy}-${mm}-${dd} ${HH}:${MM}`;
};

export const timestampToString = (timestamp) => {
  const date = new Date(timestamp * 1000);
  return dateToString(date);
};

export const dateToDuration = (d, since) => {
  const endDate = since || new Date();

  const diffMs = endDate - d;
  const diffMins = Math.floor(diffMs / 1000 / 60);
  let diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);
  diffHours -= diffDays * 24;
  const remainingMins = diffMins % 60;

  let durationString = "";
  if (diffDays > 0) {
    durationString += diffDays + "d ";
  }
  if (diffHours > 0) {
    durationString += diffHours + "h ";
  }
  if (remainingMins > 0 && diffDays === 0) {
    durationString += remainingMins + "m ";
  }

  durationString = durationString.trim();

  if (!durationString.length) {
    return Math.floor(diffMs / 1000) + "s";
  }

  return durationString;
};

export const timestampToDuration = (timestamp, since) => {
  let sinceDate = since ? new Date(since * 1000) : null;
  const date = new Date(timestamp * 1000);
  return dateToDuration(date, sinceDate);
};
