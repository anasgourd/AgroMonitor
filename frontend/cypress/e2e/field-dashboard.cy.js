describe("Home Page", () => {
    it("displays the fields and summary information", () => {
        cy.visit("http://localhost:5173");

        cy.contains("Μπέης").should("be.visible");
        cy.contains("Βαίτσα").should("be.visible");
        cy.contains("Ευανθία").should("be.visible");

        cy.contains("Total Fields").should("be.visible");
        cy.contains("Active Sensors").should("be.visible");
        cy.contains("Open Alerts").should("be.visible");
    });
});

describe("Home Page", () => {
    it("displays the correct summary values", () => {
        cy.visit("http://localhost:5173");

        cy.contains("Total Fields")
            .parent()
            .should("contain", "3");

        cy.contains("Active Sensors")
            .parent()
            .should("contain", "12");

        cy.contains("Open Alerts")
            .parent()
            .should("contain", "2");
    });
});


describe("Field Dashboard", () => {
    it("opens the field dashboard", () => {
        cy.visit("http://localhost:5173");

        cy.contains("View Field").click();

        cy.contains("FIELD DASHBOARD").should("be.visible");
        cy.contains("Μπέης").should("be.visible");
    });
});

describe("Field Dashboard", () => {
    it("displays the main dashboard sections", () => {
        cy.visit("http://localhost:5173");

        cy.contains("View Field").click();

        // Map
        cy.contains("Field Map").should("be.visible");

        // Historical analysis
        cy.contains("Temperature history").should("be.visible");
        cy.contains("Humidity history").should("be.visible");

        // Sensor sections
        cy.contains("Connected sensors").should("be.visible");
    });
});

describe("Field Dashboard", () => {
  it("returns to the home page when clicking Back", () => {
    cy.visit("http://localhost:5173");

    cy.contains("View Field").click();

    cy.contains("Μπέης").should("be.visible");

    cy.contains("Back to My Fields").click();

    cy.contains("Total Fields").should("be.visible");
    cy.contains("Active Sensors").should("be.visible");
    cy.contains("Open Alerts").should("be.visible");
  });
});