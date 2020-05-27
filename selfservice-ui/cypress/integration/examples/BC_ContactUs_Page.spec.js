describe('Home Page', function()
{
    it('Visits the Home page', function()
    {
        cy.log("Visiting the BC Services Card [DEV] URL")
        cy.visit('https://selfservice-dev.pathfinder.gov.bc.ca/')
        cy.wait(5000)
        //If clicked on Contact US, It should allow to click back
        cy.log("Click on Contact Us opens a URL in the same window")
        cy.get('[href="/contact-us"]').click()  
        cy.wait(5000)
        cy.log("Should take user to Contact Us Page")
        cy.url().should('eq','https://selfservice-dev.pathfinder.gov.bc.ca/contact-us')
        cy.wait(2000)
        cy.log("Submit Contact details")
        cy.get('input[data-test-id="input-firstname"]').type('FirstName')
        cy.wait(5000)
        cy.get('input[data-test-id="input-lastname"]').type('LastName')
        cy.wait(5000)
        cy.log("Email should be of the format '@gov.bc.ca'")
        cy.get('input[data-test-id="input-email"]').type('email@gov.bc.ca')
        .should('include.value','@gov.bc.ca')
        cy.get('textarea[data-test-id="text-contact-us-description"]').type('Testing Contact us Page')
        cy.wait(5000)
        cy.log("Submit Request")
        cy.get('[data-test-id="btn-contact-us"]').click()
        cy.wait(3000)
        cy.scrollTo("top")
        cy.log("success Message content")
        cy.contains('Your message has been sent successfully to IDIM.')
        cy.wait(5000)
        cy.log("Clicking on back button should take user Back to Home Page")
        cy.go('back')  
        cy.wait(5000)
        cy.visit('https://selfservice-dev.pathfinder.gov.bc.ca/')
        cy.log("Test Complete")
    })
    
})