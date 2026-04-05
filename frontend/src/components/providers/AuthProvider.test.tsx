import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";

import { AuthProvider } from "./AuthProvider";

describe("AuthProvider local auth mode", () => {
  beforeEach(() => {
    sessionStorage.clear();
    localStorage.clear();
    vi.stubEnv("NEXT_PUBLIC_AUTH_MODE", "local");
  });

  afterEach(() => {
    vi.unstubAllEnvs();
    vi.restoreAllMocks();
    sessionStorage.clear();
    localStorage.clear();
  });

  it("renders the login gate when no local token exists", async () => {
    render(
      <AuthProvider>
        <div>app shell</div>
      </AuthProvider>,
    );

    await waitFor(() =>
      expect(
        screen.getByRole("heading", { name: /local authentication/i }),
      ).toBeInTheDocument(),
    );
    expect(screen.queryByText("app shell")).not.toBeInTheDocument();
  });

  it("renders children when a token exists in localStorage", async () => {
    localStorage.setItem("mc_local_auth_token", "x".repeat(50));

    render(
      <AuthProvider>
        <div>app shell</div>
      </AuthProvider>,
    );

    await waitFor(() =>
      expect(screen.getByText("app shell")).toBeInTheDocument(),
    );
    expect(
      screen.queryByRole("heading", { name: /local authentication/i }),
    ).not.toBeInTheDocument();
    expect(sessionStorage.getItem("mc_local_auth_token")).toBe("x".repeat(50));
  });
});
