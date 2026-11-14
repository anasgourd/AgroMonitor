import { describe, it, expect } from "vitest";
import { calculateAverage, statusStyles, } from "../utils/fieldUtils";
import { aggregateFieldTemperature } from "../utils/fieldUtils";

describe("calculateAverage", () => {
    it("calculates the average value of active sensors", () => {
        const sensors = [
            { value: 28, status: "active" },
            { value: 30, status: "active" },
            { value: 32, status: "active" },
        ];

        expect(calculateAverage(sensors)).toBe(30);
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






describe("aggregateFieldTemperature", () => {
    it("averages each sensor first, then averages sensors per minute", () => {
        const measurements = {
            3: [
                { value: 10, unit: "C", timestamp: "2026-10-28T10:00:01Z" },
                { value: 20, unit: "C", timestamp: "2026-10-28T10:00:02Z" },
            ],
            4: [
                { value: 30, unit: "C", timestamp: "2026-10-28T10:00:03Z" },
            ],
        };

        expect(aggregateFieldTemperature(measurements)).toEqual([
            {
                time: "2026-10-28T10:00:00.000Z",
                value: 22.5,
            },
        ]);
    });

    it("keeps a single sensor's value and sorts timestamps", () => {
        const measurements = {
            3: [
                { value: 80, unit: "C", timestamp: "2026-10-28T10:02:00Z" },
                { value: 70, unit: "C", timestamp: "2026-10-28T10:00:00Z" },
            ],
        };

        expect(aggregateFieldTemperature(measurements)).toEqual([
            { time: "2026-10-28T10:00:00.000Z", value: 70 },
            { time: "2026-10-28T10:02:00.000Z", value: 80 },
        ]);
    });

    it("ignores other units and invalid values", () => {
        const measurements = {
            3: [
                { value: 50, unit: "%", timestamp: "2026-10-28T10:00:00Z" },
                { value: "invalid", unit: "C", timestamp: "2026-10-28T10:00:00Z" },
            ],
        };

        expect(aggregateFieldTemperature(measurements)).toEqual([]);
    });
});

