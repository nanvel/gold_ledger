import { useAuthStore } from "@/stores/auth";
import { useToast } from "vue-toastification";

export const httpClient = {
  get: request("GET"),
  post: request("POST"),
  put: request("PUT"),
  delete: request("DELETE"),
};

function request(method) {
  return (url, data, body, contentType) => {
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
    return fetch(url, requestOptions).then(handleResponse);
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

async function handleResponse(response) {
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

    const toast = useToast();
    // get error message from body or default to response status
    if (response.status === 500) {
      toast.error("Internal server error.");
    } else {
      toast.error(data?.message || response.status.toString());
    }

    return Promise.reject(data);
  }

  return data;
}
