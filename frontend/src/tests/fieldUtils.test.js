import { describe, it, expect } from "vitest";
import { calculateAverage, statusStyles, } from "../utils/fieldUtils";

describe("calculateAverage", () => {
    it("calculates the average sensor value", () => {
        const sensors = [
            { value: 28 },
            { value: 30 },
            { value: 32 },
        ];

        expect(calculateAverage(sensors)).toBe(30);
    });

    it("returns 0 when there are no sensors", () => {
        expect(calculateAverage([])).toBe(0);
    });
});

describe("statusStyles", () => {
    it("contains styles and message for Healthy status", () => {
        expect(statusStyles.Healthy).toBeDefined();
        expect(statusStyles.Healthy.badge).toBeDefined();
        expect(statusStyles.Healthy.dot).toBeDefined();
        expect(statusStyles.Healthy.message).toBeDefined();
    });

    it("contains styles and message for Attention status", () => {
        expect(statusStyles.Attention).toBeDefined();
        expect(statusStyles.Attention.badge).toBeDefined();
        expect(statusStyles.Attention.dot).toBeDefined();
        expect(statusStyles.Attention.message).toBeDefined();
    });

    it("contains styles and message for Alert status", () => {
        expect(statusStyles.Alert).toBeDefined();
        expect(statusStyles.Alert.badge).toBeDefined();
        expect(statusStyles.Alert.dot).toBeDefined();
        expect(statusStyles.Alert.message).toBeDefined();
    });
});


