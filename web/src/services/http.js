import { useAuthStore } from "@/stores/auth";
import { useToast } from "vue-toastification";

export const httpClient = {
  get: request("GET"),
  post: request("POST"),
  put: request("PUT"),
  delete: request("DELETE"),
};

export const parseError = (message, field) => {
  if (!message?.detail && !field) {
    return "An error occurred";
  }
  const detail = message?.detail;
  const isString = typeof detail === "string" || detail instanceof String;
  if (!field && isString) {
    return detail;
  }
  if (field && !isString) {
    return detail.find((d) => d.loc[1] === field)?.msg;
  }
};

function request(method) {
  return (url, data, body, args) => {
    const { contentType = null } = args || {};
    const requestOptions = {
      method,
      headers: authHeader(url),
    };
    if (data) {
      requestOptions.headers["Content-Type"] = "application/json";
      requestOptions.body = JSON.stringify(data);
    }
    if (body) {
      requestOptions.body = body;
    }
    if (contentType) {
      requestOptions.headers["Content-Type"] = contentType;
    }
    return fetch(url, requestOptions).then((resp) =>
      handleResponse(resp, args),
    );
  };
}

// helper functions

function authHeader(url) {
  // return auth header with jwt if user is logged in and request is to the api url
  const { authToken } = useAuthStore();
  const isLoggedIn = !!authToken;
  const isApiUrl = url.startsWith("/api");
  if (isLoggedIn && isApiUrl) {
    return { Authorization: `Bearer ${authToken}` };
  } else {
    return {};
  }
}

async function handleResponse(response, args) {
  const { showToast = true } = args || {};
  const isJson = response.headers
    ?.get("content-type")
    ?.includes("application/json");
  const data = isJson ? await response.json() : null;

  // check for error response
  if (!response.ok) {
    const { logout } = useAuthStore();
    if ([401, 403].includes(response.status)) {
      // auto logout if 401 Unauthorized or 403 Forbidden response returned from api
      await logout();
    }

    if (showToast) {
      const toast = useToast();
      // get error message from body or default to response status
      if (response.status === 500) {
        toast.error("Internal server error");
      } else if (response.status === 413) {
        toast.error("File size should less than 5MB");
      } else {
        toast.error(
          (data?.detail &&
            (typeof data.detail === "string" ||
              data.detail instanceof String) &&
            data.detail) ||
            response.status.toString(),
        );
      }
    }

    if (response.status === 413) {
      return Promise.reject({ detail: "File size should less than 5MB" });
    }

    return Promise.reject(data);
  }

  return data;
}

export async function downloadFile(url) {
  const res = await fetch(url, { headers: authHeader(url) });
  const disposition = res.headers.get("Content-Disposition");
  let filename = disposition.split(/;(.+)/)[1].split(/=(.+)/)[1];
  if (filename.toLowerCase().startsWith("utf-8''")) {
    filename = decodeURIComponent(filename.replace(/utf-8''/i, ""));
  } else {
    filename = filename.replace(/['"]/g, "");
  }
  const objectUrl = window.URL.createObjectURL(await res.blob());
  const a = document.createElement("a");
  try {
    a.href = objectUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
  } finally {
    a.remove();
  }
}
