import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import FieldCard from "../components/FieldCard";

describe("FieldCard XSS protection", () => {
    it("renders malicious field names as plain text", () => {
        const payload = '<img src=x onerror=alert("XSS")>';

        const field = {
            id: 1,
            name: payload,
            type: "Test",
            area: 10,
            status: "Healthy",
        };

        const { container } = render(
            <FieldCard
                field={field}
                onSelect={vi.fn()}
                onEdit={vi.fn()}
                onDelete={vi.fn()}
                isMonitoring={false}
            />
        );

        expect(screen.getByText(payload)).toBeTruthy();
        expect(container.querySelector("img")).toBeNull();
    });
});