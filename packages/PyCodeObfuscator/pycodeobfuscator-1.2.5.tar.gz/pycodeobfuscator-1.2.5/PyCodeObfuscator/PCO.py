import sys, os, re, argparse
from termcolor import colored
from base64 import b16encode, b32encode, b64encode, b85encode, b16decode, b32decode, b64decode, b85decode
import zlib, gzip, bz2
from random import choice

class Data:



    def __init__(self):



        self.encoding_formats = {
            b16encode: b16decode,
            b32encode: b32decode,
            b64encode: b64decode,
            b85encode: b85decode,
            zlib.compress: zlib.decompress,
            gzip.compress: gzip.decompress,
            bz2.compress: bz2.decompress
        }



        self.variable_names = [
            "god", "light", "hope", "blessing", "trust", "remember", "faith", "grace", "truth", "love",
            "peace", "kindness", "justice", "mercy", "charity", "freedom", "wisdom", "purity", "honor", "valor",
            "strength", "forgiveness", "joy", "humility", "unity", "courage", "compassion", "serenity", "devotion",
            "dignity", "harmony", "eternity", "reverence", "integrity", "virtue", "loyalty", "confidence", "redemption",
            "patience", "sacrifice", "gratitude", "benevolence", "hopefulness", "sincerity", "providence", "sanctity", "fortitude",
            "holiness", "dedication", "goodness", "prayer", "belief", "lightness", "purification", "understanding", "contentment",
            "faithfulness", "reliance", "bliss", "magnanimity", "friendship", "equity", "empowerment", "healing", "perseverance",
            "bravery", "truthfulness", "inspiration", "aspiration", "guidance", "upliftment", "altruism", "encouragement", "enlightenment",
            "celebration", "clarity", "kindheartedness", "honesty", "tolerance", "euphoria", "delight", "trustworthiness", "resolve",
            "motivation", "radiance", "jubilation", "peacefulness", "sanctuary", "fulfillment", "empathy", "dedication", "renewal",
            "acceptance", "hopefulness", "reflection", "awareness", "admiration", "prosperity", "resolve", "reliability", "transcendence",
            "allegiance", "generosity", "inclusion", "nobility", "positivity", "balance", "creativity", "humbleness", "tranquility",
            "infallibility", "benevolence", "patience", "selflessness", "radiance", "vitality", "equanimity", "focus", "satisfaction",
            "pride", "zest", "moderation", "resourcefulness", "intuition", "optimism", "justice", "compassionate", "dreamer", 
            "perfection", "heroism", "illumination", "initiative", "mindfulness", "sympathy", "understanding", "vision", "solidarity", 
            "warmth", "tenacity", "resilience"
        ]



    def encodeRandom(self, data):
        encodefunction, decodefunction = choice(list(self.encoding_formats.items()))

        try:
            if encodefunction in [b16encode, b32encode, b64encode, b85encode, zlib.compress, gzip.compress, bz2.compress]:
                encodedData = encodefunction(data.encode('utf-8'))
            else:
                encodedData = encodefunction(data)

            decodefunction_string = f"{decodefunction.__module__}.{decodefunction.__name__}"
            return encodedData, decodefunction_string

        except Exception as e:
            return f"[ERROR] Encoding failed: {e}", None

class File:



    def __init__(self, file_path, verbose: bool):
        self.file_path = file_path
        self.content = self.load_file()
        self.verbose = verbose



    def load_file(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(colored("[ERROR]", "red"), f"Error: File '{self.file_path}' not found.")
            sys.exit(1)
        except Exception as e:
            print(colored("[ERROR]", "red"), f"An error occurred: {e}")
            sys.exit(1)



    def obfuscate(self):
        data = Data()

        error = colored("[ERROR]", "red")
        info = colored("[INFO]", "green")
        if self.verbose:
            print(info, f"Obfuscating file: {self.file_path}")

        self.content = re.sub(r"(?m)^\s*#.*$", "", self.content)
        self.content = re.sub(r"(?s)'''.*?'''", "", self.content)
        self.content = re.sub(r'(?s)""".*?"""', "", self.content)

        self.content = re.sub("\n\n", "\n", self.content)

        self.content_lines = self.content.split("\n")

        if len(self.content_lines) < 5:
            self.varaible_count = 1
        elif len(self.content_lines) <= 30:
            self.varaible_count = len(self.content_lines) // 5
        elif len(self.content_lines) <= 100:
            self.varaible_count = len(self.content_lines) // 15
        elif len(self.content_lines) <= 500:
            self.varaible_count = len(self.content_lines) // 50
        elif len(self.content_lines) <= 20000:
            self.varaible_count = len(self.content_lines) // 500
        else:
            self.varaible_count = 40
        
        self.varaible_count = min(self.varaible_count, len(self.content_lines))
        if self.verbose:
            print(info, f"Content will be split into {self.varaible_count} variables")

        varaible_size = (len(self.content_lines) + self.varaible_count - 1) // self.varaible_count
        self.variable_lines = [self.content_lines[i * varaible_size:(i + 1) * varaible_size] for i in range(self.varaible_count)]
        self.variables = ['\n'.join(var) for var in self.variable_lines]

        if self.verbose:
            print(info, f"Content has been split into {len(self.variables)} variables")

        if self.verbose:
            print(info, f"Obfuscating Content...")
        self.full_variables = {}
        for i in range(len(self.variables)):
            encoded_data, decoding_function = data.encodeRandom(self.variables[i])
            if self.verbose:
                print(info, f"Encoded variable {i + 1}, decode using {decoding_function}")
            var_name = choice(data.variable_names)
            data.variable_names.remove(var_name)
            self.full_variables[(var_name, decoding_function)] = f"{var_name} = {encoded_data}"

        if self.verbose:
            print(info, f"Generating Decoding functions...")
        self.decodestrings ={}
        for (var_name, var_decodefunc), encoded_data in self.full_variables.items():
            decode_varname = choice(data.variable_names)
            data.variable_names.remove(decode_varname)
            decodestring = f"{decode_varname} = {var_decodefunc}({var_name})"
            self.decodestrings[decode_varname] = decodestring
        
        if self.verbose:
            print(info, f"Initializing content...")
        self.content = "import zlib, gzip, bz2, base64"

        if self.verbose:
            print(info, f"Adding Encoded variables...")
        for variable in self.full_variables.values():
            self.content += f"\n{variable}"

        if self.verbose:
            print(info, f"Generating Exec()...")
        final_exec = "exec("
        for decodevaraible, decodestring in self.decodestrings.items():
            self.content += f"\n{decodestring}"
            final_exec += f"{decodevaraible}.decode('utf-8') + '\\n' + "
        if self.verbose:
            print(info, f"Trimming content...")
        self.content += f"\n{final_exec[:-10]})"






    def save(self):
        base, ext = os.path.splitext(self.file_path)
        new_file_path = f"{base}_obf{ext}"
        with open(new_file_path, "w", encoding="utf-8") as f:
            f.write(self.content)
        print(colored("[INFO]", "green"), f"Obfuscated file saved as: {new_file_path}")
        return new_file_path



def main():
    error = colored("[ERROR]", "red")
    info = colored("[INFO]", "green")
    
    parser = argparse.ArgumentParser(description="PyCodeObfuscator Script")
    parser.add_argument("file", metavar="file", type=str, help="Path to the file to be obfuscated")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output, may affect performance on older machines")
    parser.add_argument("-s", "--single", action="store_true", help="Only runs the obfuscator one iteration (Only obfuscates once)")
    args = parser.parse_args()
    
    file_path = args.file
    if args.verbose:
        print(info, f"Loading file: {file_path}")
    
    try:
        file = File(file_path, args.verbose)
        if not args.single:
            for i in range(20):
                print(info, f"Obfuscating, Iteration: {i+1}/20")
                file.obfuscate()
        print(info, f"Obfuscating...")
        file.obfuscate()
        new_file_path = file.save()
        print(info, f"File successfully obfuscated! Result Character Lenght: {len(file.content)}")
        
        if args.verbose:
            print(info, "File obfuscated and saved successfully")
        
    except Exception as e:
        print(error, "An error occurred:", e)



if __name__ == "__main__":
    main()
