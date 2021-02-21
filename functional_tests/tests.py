from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Kirsten has heard of a cool new online app for managing VLS workflow.
        # She goes to check out its homepage.
        self.browser.get('http://localhost:8000')

        # She notices the page title mentions webinar workflow and 
        # the header mentions webinar to-do lists
        self.assertIn('Webinar Workflow', self.browser.title)
        header_text = self.browser.find_elements_by_tag_name('h1')[0].text
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
        self.check_for_row_in_list_table('1: Schedule Zoom meeting')
            
        # There is still a text box inviting her to add another item. She
        # enters "Schedule invitation email campaign"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Schedule invitation email campaign')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Schedule Zoom meeting')
        self.check_for_row_in_list_table('2: Schedule invitation email campaign')
        
        # Kirsten wonders whether the site will remember her list. Then
        # she sees that the site has generated a unique URL for her -- there
        # is some explanatory text to that effect.
        self.fail('Finish the test!')        
        
        # She visits that URL - her to-do list is still there.
        
        # Satisfied, she closes the web browser.

if __name__ == '__main__':
    unittest.main()