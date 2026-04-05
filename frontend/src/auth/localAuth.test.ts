import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import {
  clearLocalAuthToken,
  getLocalAuthToken,
  setLocalAuthToken,
} from "./localAuth";

describe("localAuth storage", () => {
  beforeEach(() => {
    clearLocalAuthToken();
    sessionStorage.clear();
    localStorage.clear();
  });

  afterEach(() => {
    clearLocalAuthToken();
    vi.restoreAllMocks();
  });

  it("stores tokens in both sessionStorage and localStorage", () => {
    const token = "p".repeat(50);

    setLocalAuthToken(token);

    expect(sessionStorage.getItem("mc_local_auth_token")).toBe(token);
    expect(localStorage.getItem("mc_local_auth_token")).toBe(token);
    expect(getLocalAuthToken()).toBe(token);
  });

  it("rehydrates from localStorage into sessionStorage", () => {
    const token = "q".repeat(50);

    localStorage.setItem("mc_local_auth_token", token);

    expect(getLocalAuthToken()).toBe(token);
    expect(sessionStorage.getItem("mc_local_auth_token")).toBe(token);
  });

  it("clears persisted tokens from both storage layers", () => {
    const token = "r".repeat(50);

    setLocalAuthToken(token);
    clearLocalAuthToken();

    expect(getLocalAuthToken()).toBeNull();
    expect(sessionStorage.getItem("mc_local_auth_token")).toBeNull();
    expect(localStorage.getItem("mc_local_auth_token")).toBeNull();
  });
});
