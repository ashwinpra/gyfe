A simple script to find the electives available for you, given your elective slots

---

## Usage 
- This script uses the [iit-kgp-erp-login](https://pypi.org/project/iitkgp-erp-login/) library created by [proffapt](https://github.com/proffapt), and as such, there is some pre-requisite setup to be done 
    - Create the `erpcreds.py` file following the instructions [here](https://pypi.org/project/iitkgp-erp-login/#erpcreds)
    - Generate `token.json` file following the instructions [here](https://pypi.org/project/iitkgp-erp-login/#token)
- Install dependencies by running 
```sh
pip install -r requirements.txt
```
- Run the main script following the format: 
```sh
python3 main.py --slots <list-of-slots>
```
- This will generate a file called `electives.csv` with all the electives, along with `available-electives.txt`, which will list the electives available to you (based on your slots)
- Additionally, to overwrite an old `electives.csv` file, run the script with an additional `-o` flag. For example:
```sh
python3 main.py -o --slots F3 
```


## Example
```py
python3 main.py --slots F4 G3
```
- `available-electives.txt`:
<img src="./sample_output.png">

#
### Future plans
- Add a version which does not require Gmail API usage (ie. user would enter OTP manually)
- Make it a web app for ease of use
