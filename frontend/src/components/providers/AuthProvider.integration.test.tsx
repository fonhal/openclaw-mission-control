import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { AuthProvider } from "./AuthProvider";

const fetchMock = vi.hoisted(() => vi.fn());

beforeEach(() => {
  sessionStorage.clear();
  localStorage.clear();
  fetchMock.mockReset();
  vi.stubGlobal("fetch", fetchMock);
  vi.stubEnv("NEXT_PUBLIC_AUTH_MODE", "local");
  vi.stubEnv("NEXT_PUBLIC_API_URL", "http://localhost:8000/");
});

afterEach(() => {
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
  vi.restoreAllMocks();
  sessionStorage.clear();
  localStorage.clear();
});

describe("AuthProvider integration", () => {
  it("unlocks the app after a successful local login", async () => {
    fetchMock.mockResolvedValueOnce(new Response(null, { status: 200 }));
    const user = userEvent.setup();

    render(
      <AuthProvider>
        <div>secured app shell</div>
      </AuthProvider>,
    );

    await waitFor(() =>
      expect(
        screen.getByRole("heading", { name: /local authentication/i }),
      ).toBeInTheDocument(),
    );

    await user.type(
      screen.getByPlaceholderText("Paste token or Bearer token"),
      "z".repeat(50),
    );
    await user.click(screen.getByRole("button", { name: "Continue" }));

    await waitFor(() =>
      expect(fetchMock).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/users/me",
        expect.objectContaining({
          method: "GET",
          headers: { Authorization: `Bearer ${"z".repeat(50)}` },
        }),
      ),
    );

    await waitFor(() =>
      expect(localStorage.getItem("mc_local_auth_token")).toBe("z".repeat(50)),
    );
  });
});
