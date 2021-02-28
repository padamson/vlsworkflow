from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def test_can_start_a_list_for_one_webinar(self):
        # Edith has heard of a cool new online app for managing VLS workflow.
        # She goes to check out its homepage.
        self.browser.get(self.live_server_url)

        # She notices the page title mentions webinar workflow and 
        # the header mentions webinar to-do lists
        self.assertIn('Webinar Workflow', self.browser.title)
        header_text = self.browser.find_elements_by_tag_name('h1')[0].text
        self.assertIn('Start a new webinar to-do list', header_text)

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
        self.wait_for_row_in_list_table('1: Schedule Zoom meeting')
            
        # There is still a text box inviting her to add another item. She
        # enters "Schedule invitation email campaign"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Schedule invitation email campaign')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on the webinar list
        self.wait_for_row_in_list_table('2: Schedule invitation email campaign')
        self.wait_for_row_in_list_table('1: Schedule Zoom meeting')
        
        # Satisfied, she closes the web browser.

    def test_multiple_users_can_start_webinar_list_at_different_urls(self):
        # Edith starts a new webinar to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Schedule April Zoom meeting')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Schedule April Zoom meeting')

        # She notices that the site has generated a unique URL for her
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/webinars/.+')
        
        # Now a new user, Francis, comes along to the site.
        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()
    
        # Francis visits the home page.  There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Schedule April Zoom meeting', page_text)
        self.assertNotIn('Schedule invitation email campaign', page_text)
    
        # Francis starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Schedule May Zoom meeting')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Schedule May Zoom meeting')
    
        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/webinars/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)
    
        # Again, there is no trace of Edith's list, and Francis's is there
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Schedule April Zoom meeting', page_text)
        self.assertIn('Schedule May Zoom meeting', page_text)
    
        # Satisfied, they both close their browsers
        self.fail('Finish the test!')        
