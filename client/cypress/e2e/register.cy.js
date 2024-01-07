import "cypress-real-events/support";

describe("User Registration and Login Workflow", () => {
  const baseApiUrl = "http://localhost:8080/api/postgres"
  const baseClientUrl = "http://localhost:3000"

  const userEmail = "cypress-test@test.com";
  const userPassword = "password";
  let accessToken = "";

  it("Registers a new user", () => {
    cy.intercept("POST", `${baseApiUrl}/auth/register`).as("userRegistration");

    cy.visit(`${baseClientUrl}/login`);
    cy.get("a:nth-child(1)").click();
    cy.url().should("include", "/register");

    cy.get("input[type='email']").type(userEmail);
    cy.get("input[type='password']:first").type(userPassword);
    cy.get("input[type='password']:last").type(userPassword);
    cy.get("button[type='submit']").click();

    cy.checkAlert("Registration successful");

    cy.wait("@userRegistration");
    cy.url().should("include", "/login");
  });

  /*   it("Attempts to register a new user with an existing email", () => {
      cy.intercept("POST", `${baseApiUrl}/auth/register`).as("userRegistration");
  
      cy.visit(`${baseClientUrl}/login`);
      cy.get("a:nth-child(1)").click();
      cy.url().should("include", "/register");
  
      cy.get("input[type='email']").type(userEmail);
      cy.get("input[type='password']:first").type(userPassword);
      cy.get("input[type='password']:last").type(userPassword);
      cy.get("button[type='submit']").click();
  
      cy.on('window:alert', (text) => {
        expect(text).to.equal("Error: User already exists");
      });
  
      cy.wait("@userRegistration");
      cy.url().should("include", "/login");
    }); */

  it("Attempts to register a new user with a password that is too short", () => {
    cy.visit(`${baseClientUrl}/login`);
    cy.get("a:nth-child(1)").click();
    cy.url().should("include", "/register");

    cy.get("input[type='email']").type(userEmail);
    cy.get("input[type='password']:first").type("1");
    cy.get("input[type='password']:last").type("1");
    cy.get("button[type='submit']").click();

    cy.checkAlert("Password must be between 8 and 32 characters");
    cy.url().should("include", "/register");
  });

  it("Attempts to register a new user with a password that is too long", () => {
    cy.visit(`${baseClientUrl}/login`);
    cy.get("a:nth-child(1)").click();
    cy.url().should("include", "/register");

    cy.get("input[type='email']").type(userEmail);
    cy.get("input[type='password']:first").type("1" * 33);
    cy.get("input[type='password']:last").type("1" * 33);
    cy.get("button[type='submit']").click();

    cy.checkAlert("Password must be between 8 and 32 characters");
    cy.url().should("include", "/register");
  });

  it("Attempts to register a new user with an invalid email input", () => {
    cy.visit(`${baseClientUrl}/register`);
    cy.get("input[type='email']").type("test");
    cy.get("input[type='password']:first").type(userPassword);
    cy.get("input[type='password']:last").type(userPassword);
    cy.get("button[type='submit']").click();

    cy.get("input[type='email']").should('have.prop', 'validity').then((validity) => {
      expect(validity.valid).to.be.false;
      expect(validity.typeMismatch).to.be.true;
    });
    cy.url().should("include", "/register");
  });

  /*   it("Attempts to register a new user without filling out all fields", () => {
      cy.visit(`${baseClientUrl}/login`);
      cy.get("a:nth-child(1)").click();
      cy.url().should("include", "/register");
  
      cy.get("button[type='submit']").click();
  
      cy.on('window:alert', (text) => {
        expect(text).to.equal("Please fill out all fields");
      });
  
      cy.url().should("include", "/register");
    }); */

  it("Logs the registered user in", () => {
    cy.intercept("POST", `${baseApiUrl}/auth/login-email`).as("userLogin");

    cy.visit(`${baseClientUrl}/login`);
    cy.get("input[type='email']").clear().type(userEmail);
    cy.get("input[type='password']").clear().type(userPassword);
    cy.get("button[type='submit']").click();

    cy.wait("@userLogin").then(({ response }) => {
      accessToken = response.body.data.access_token;
    });

    cy.url().should("include", "/characters");
  });

  after(() => {
    if (accessToken) {
      cy.deleteCurrentUser(accessToken)
    }
  });
});