from robocorp.tasks import task
from robocorp import browser
from robocorp.tasks import get_output_dir
from RPA.Browser.Selenium import Selenium 


@task
def minimal_task():
    # browser = Selenium(auto_close = False)
    # browser.open_available_browser('https://www.google.co.uk')
    browser = Selenium(auto_close = False)
    browser.open_available_browser('https://www.google.co.uk')
    try:
        browser.click_button('Accept all')
    except:
        pass
    browser.input_text('name:q','rpaframework')
    browser.click_button('Google Search',"ENTER")
    # browser.input_text('name:q','rpaframework' + "ENTER")
    # 

#     <textarea class="gLFyf" aria-controls="Alh6id" aria-owns="Alh6id" autofocus="" title="Search" value="" jsaction="paste:puy29d;" aria-label="Search" aria-autocomplete="both" aria-expanded="false" aria-haspopup="false" autocapitalize="off" autocomplete="off" autocorrect="off" id="APjFqb" maxlength="2048" name="q" role="combobox" rows="1" spellcheck="false" data-ved="0ahUKEwie-97TmsCFAxVEzAIHHcFLBIEQ39UDCAQ"></textarea>
# <textarea class="gLFyf" aria-controls="Alh6id" aria-owns="Alh6id" autofocus="" title="Search" value="" jsaction="paste:puy29d;" aria-label="Search" aria-autocomplete="both" aria-expanded="true" aria-haspopup="false" autocapitalize="off" autocomplete="off" autocorrect="off" id="APjFqb" maxlength="2048" name="q" role="combobox" rows="1" spellcheck="false" data-ved="0ahUKEwjUj-yLm8CFAxWP6wIHHc3QCioQ39UDCAQ" aria-activedescendant="" style=""></textarea>
# //*[@id="APjFqb"]
# <input class="gNO89b" value="Google Search" aria-label="Google Search" name="btnK" role="button" tabindex="0" type="submit" data-ved="0ahUKEwjUj-yLm8CFAxWP6wIHHc3QCioQ4dUDCBE">
    # browser.configure(
    #    browser_engine="chromium", 
    #    screenshot="only-on-failure",
    #    headless= False,

    #    )
    # page = browser.goto("https://www.google.co.uk")
    # page.fill("//input[@name='q']", 'rpaframework')
    # page.click("input:text('Google Search')")