from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Kirsten has heard of a cool new online app for managing VLS workflow.
        # She goes to check out its homepage.
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mentions to-do
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_elements_by_tag_name('h1').text
        self.assertIn('Webinar To-Do Lists', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
    
        # She types "Schedule Zoom meeting" into a text box
        inputbox.send_keys('Schedule Zoom meeting')
        
        # When she hits enter, the page updates, and now the page lists
        # "1: Schedule Zoom meeting" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Schedule Zoom meeting' for row in rows)
        )
            
        # There is still a text box inviting her to add another item. She
        # enters "Schedule invitation email campaign"
        self.fail('Finish the test!')        

        # The page updates again, and now shows both items on her list
        
        # Kirsten wonders whether the site will remember her list. Then
        # she sees that the site has generated a unique URL for her -- there
        # is some explanatory text to that effect.
        
        # She visits that URL - her to-do list is still there.
        
        # Satisfied, she closes the web browser.

if __name__ == '__main__':
    unittest.main()