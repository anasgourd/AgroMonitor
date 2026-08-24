export const fields = [
  {
    id: 1,
    name: "Μπέης",
    type: "Oranges",
    area: "12.5 ha",

    sensorDetails: [
      {
        id: "T-01",
        type: "Temperature",
        value: 28,
        unit: "°C",
        status: "Normal",
      },
      {
        id: "T-02",
        type: "Temperature",
        value: 28.4,
        unit: "°C",
        status: "Normal",
      },
      {
        id: "T-03",
        type: "Temperature",
        value: 27.7,
        unit: "°C",
        status: "Normal",
      },
      {
        id: "H-01",
        type: "Humidity",
        value: 42,
        unit: "%",
        status: "Normal",
      },
      {
        id: "H-02",
        type: "Humidity",
        value: 44,
        unit: "%",
        status: "Normal",
      },
    ],

    history: {
      temperature: [
        { time: "08:00", value: 25.6 },
        { time: "10:00", value: 26.8 },
        { time: "12:00", value: 27.8 },
        { time: "14:00", value: 28.6 },
        { time: "16:00", value: 28.2 },
        { time: "18:00", value: 28.0 },
      ],

      humidity: [
        { time: "08:00", value: 50 },
        { time: "10:00", value: 47 },
        { time: "12:00", value: 44 },
        { time: "14:00", value: 41 },
        { time: "16:00", value: 43 },
        { time: "18:00", value: 42 },
      ],
    },



    status: "Healthy",
  },

  // τα υπόλοιπα fields προσωρινά όπως είναι

  {
    id: 2,
    name: "Βαίτσα",
    type: "Olive Grove",
    area: "8.2 ha",

    sensorDetails: [
      {
        id: "T-01",
        type: "Temperature",
        value: 31,
        unit: "°C",
        status: "Normal",
      },
      {
        id: "T-02",
        type: "Temperature",
        value: 31.4,
        unit: "°C",
        status: "Normal",
      },
      {
        id: "H-01",
        type: "Humidity",
        value: 27,
        unit: "%",
        status: "Normal",
      },
      {
        id: "H-02",
        type: "Humidity",
        value: 29,
        unit: "%",
        status: "Normal",
      },
    ],

    history: {
      temperature: [
        { time: "08:00", value: 28.6 },
        { time: "10:00", value: 29.8 },
        { time: "12:00", value: 30.8 },
        { time: "14:00", value: 31.6 },
        { time: "16:00", value: 31.2 },
        { time: "18:00", value: 31.0 },
      ],

      humidity: [
        { time: "08:00", value: 35 },
        { time: "10:00", value: 32 },
        { time: "12:00", value: 29 },
        { time: "14:00", value: 26 },
        { time: "16:00", value: 28 },
        { time: "18:00", value: 27 },
      ],
    },



    status: "Attention",
  },

  {
    id: 3,
    name: "Ευανθία",
    type: "Oranges",
    area: "15.7 ha",

    sensorDetails: [
      {
        id: "T-01",
        type: "Temperature",
        value: 33,
        unit: "°C",
        status: "Alert",
      },
      {
        id: "H-01",
        type: "Humidity",
        value: 18,
        unit: "%",
        status: "Alert",
      },
      {
        id: "H-02",
        type: "Humidity",
        value: 20,
        unit: "%",
        status: "Alert",
      },
    ],

    history: {
      temperature: [
        { time: "08:00", value: 30.6 },
        { time: "10:00", value: 31.8 },
        { time: "12:00", value: 32.8 },
        { time: "14:00", value: 33.6 },
        { time: "16:00", value: 33.2 },
        { time: "18:00", value: 33.0 },
      ],

      humidity: [
        { time: "08:00", value: 26 },
        { time: "10:00", value: 23 },
        { time: "12:00", value: 21 },
        { time: "14:00", value: 18 },
        { time: "16:00", value: 20 },
        { time: "18:00", value: 18 },
      ],
    },



    status: "Alert",
  },


];