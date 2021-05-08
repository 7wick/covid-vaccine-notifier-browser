# Description:

It will notify you when the vaccine is available. Since most of us are using the laptop for the entire day, it will open a tab in your browser to the registration portal directly, as soon as vaccine is available for your age in your district.


# Steps to run it on your mac/linux: (Working on the windows guide)
1. Install python3 and pip3 (preffered: python3) *[follow: https://realpython.com/installing-python/]*
2. Take a pull of the main branch of this github repository by running:\
   *git clone https://github.com/7wick/covid-vaccine-notifier-browser.git covid-vaccine-notifier-browser*
3. Get into your directory:\
   *cd covid-vaccine-notifier-browser*
4. Insatll the dependencies:\
   *sh installer.sh*
5. Update the input.json file, as per your requirements. **[Important, else you will get wrong information]**:\
   *vi input.json*
   Press i on keyboard
   Start editing
   Press ESC on keyboard
   Press wq
      *Note:* You can check your inputs by running **cat input.json**
6. Run the bash script in the background:\
   *nohup $(find ~ -name "notifier_script.sh" 2> /dev/null) &*
7. Kill the process and stop the script: **[Very important, else you will keep getting notifications]**\
   *kill -9 $(ps -ef | grep notifier_script.sh | awk '{print $2}')*


# How to pull updated code:
1. kill -9 $(ps -ef | grep notifier_script.sh | awk '{print $2}')
2. cd $(find ~ -name "covid-vaccine-notifier-browser" 2> /dev/null)
3. git stash save
4. git checkout main
5. git pull

**Note:** You need to re-edit you input.json file after these step, else you will get wrong information. Follow from step 5 and 6 above
