# Get Your Freaking Electives :)
A simple script to find the depth and breadth electives available for you for subject registration

--- 

## Setup 
- This script uses the [iit-kgp-erp-login](https://pypi.org/project/iitkgp-erp-login/) library created by [proffapt](https://github.com/proffapt), and as such, there is some pre-requisite setup to be done
    - Copy the template for `erpcreds.py` by running `cp erpcreds.py.template erpcreds.py` in the terminal
    - Fill `erpcreds.py` with the relevant credentials
    - **If you want automatic OTP fetching**: Generate `token.json` file following the instructions [here](https://pypi.org/project/iitkgp-erp-login/#token)
- Install dependencies by running 
```sh
pip install -r requirements.txt
```
## Usage

- Run the `gyfe.py` script following the format: 
```sh
python3 gyfe.py <breadth/depth> --year <year-of-study> --session <session> --semester <semester>
```
- The first argument is either `breadth` or `depth`, depending on which electives you want to find
- `--year` is your year of study **(single digit)**, eg: `3`
- `--session` is in the format `YYYY-YYY`, eg: `2023-2024`
- `--semester` is either `AUTUMN` or `SPRING` 
> **Note**
> - `--session` has a default value of `2023-2024`, and `--semester`` has a default value of `SPRING`
> - This must be changed every semester
- Optional flag(s):
  - `--notp`: Don't use the `token.json` file to login, instead enter OTP manually (easier setup)
<br></br>
- This will generate either `available_breadths.txt` or `available_depths.txt` depending on the first argument


#### Example(s) 
```sh
python3 gyfe.py depth --year 3 --session 2023-2024 --semester AUTUMN
# find depth electives for 3rd year, Autumn 2023-2024, with automatic OTP fetching for login

python3 gyfe.py depth --notp --year 3 --session 2023-2024 --semester AUTUMN
# find depth electives for 3rd year, Autumn 2023-2024, with manual OTP input for login

python3 gyfe.py breadth --year 3 --session 2023-2024 --semester AUTUMN
# find breadth electives for 3rd year, Autumn 2023-2024, with automatic OTP fetching for login

python3 gyfe.py breadth --notp --year 3 --session 2023-2024 --semester AUTUMN
# find breadth electives for 3rd year, Autumn 2023-2024, with manual OTP input for login
```
- Example `available-breadths.txt`:
<img src="./sample_breadths.png">

- Example `available-depths.txt`:
<img src="./sample_depths.png">

--- 

### Future plans
- See how your timetable will look like with the electives you choose (OR somehow merge this with [what-slot](https://github.com/met-kgp/what-slot))
- Make it a web app for ease of use

