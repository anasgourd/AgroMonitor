
import http from "k6/http";
import { check } from "k6";

if (!__ENV.BASE_URL || !__ENV.JWT_TOKEN) {
    throw new Error("BASE_URL and JWT_TOKEN are required");
}

const endpoint = `${__ENV.BASE_URL}/users/me/fields`;

export const options = {
    scenarios: {
        warmup: {
            executor: "constant-arrival-rate",
            rate: 1,
            timeUnit: "1s",
            duration: "10s",
            preAllocatedVUs: 5,
            maxVUs: 5,
        },

        constant_load: {
            executor: "constant-arrival-rate",
            rate: 10,
            timeUnit: "1s",
            duration: "60s",
            preAllocatedVUs: 30,
            maxVUs: 30,
            startTime: "12s",
        },
    },

    thresholds: {
        "http_req_duration{scenario:constant_load}": ["p(95)<500"],
        "http_req_failed{scenario:constant_load}": ["rate==0"],
        "checks{scenario:constant_load}": ["rate==1"],
        "dropped_iterations{scenario:constant_load}": ["count==0"],
    },
};

export default function () {
    const response = http.get(endpoint, {
        headers: {
            Authorization: `Bearer ${__ENV.JWT_TOKEN}`,
        },
        timeout: "15s",
    });

    check(response, {
        "HTTP 200": (r) => r.status === 200,
    });
}
