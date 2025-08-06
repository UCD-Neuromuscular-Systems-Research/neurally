# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Version Control %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Created: 27/01/25 - Ruth Filan
# Updated: 22/02/25 - Ruth Filan (to address multiprocessing error)
# Updated: 23/02/25 - Ruth Filan (to add paragraph reading task)
# Updated: 01/04/25 - Ruth Filan (to update the logging process to ensure log listener is shut-down correctly)
# Updated: 05/04/25 - Ruth Filan (to add the ability to process the features for SV task)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Description %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# This script executes the Longitudinal Speech Analysis for:
# - Syllable Repetition (SR) Task
# - Passage Reading (PR) Task
# - Sustained Vowel (SV) Task
# it processes the speech features for the HD Baseline and HD Follow-Up groups.

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Import Libraries %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import logging
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib
matplotlib.use('Agg')                                       # To make the plotting work in background
import matplotlib.pyplot as plt
from IPython import get_ipython
import pandas as pd
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Import Local Libraries %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import audioProcessingHDLongitudinal
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Logger Set-Up %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Check if logging should be disabled in production
if os.environ.get("NEURALLY_NO_LOG") == "1":
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
    logging.getLogger().handlers = [NullHandler()]
    logging.getLogger().propagate = False
# Set up logging to log to both console and file in execution script:
logger = logging.getLogger()

# Clear any existing handlers:
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Set up logging to file and console:
# File Handlers:
file_handler = logging.FileHandler(r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\processing_log.txt")
file_handler.setLevel(logging.INFO)

# Console Handlers:
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define the log format:
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Apply formatter to both handlers:
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger:
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Set the overall logging level:
logger.setLevel(logging.INFO)

# Log message indicating the logging setup is complete:
logger.info("Logging setup complete.")

# Check if running in an IPython environment and log it once:
if get_ipython():
    logging.info("Running in IPython environment.")
    get_ipython().magic('reset -sf')  # Reset in IPython
else:
    logging.info("Not running in IPython environment.")
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Change Working Directory (with Error Handling) %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
working_dir = r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis"
try:
    os.chdir(working_dir)
    logger.info(f"Working directory changed successfully: {os.getcwd()}")
except Exception as e:
    logger.error(f"Error: {e}")

# Clear previous figures
plt.close('all')
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Define Paths & Create Output Directory %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#outputPath = r"C:\Users\Student\OneDrive - University College Dublin\Engineering Year 5 Semester 1\!EEEN40220 - ME Biomed Project\Speech\Results\Speech Features\groupHDLongitudinal\Features"
outputPath = r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDLongitudinal\Features"

# Ensure output directory exists
os.makedirs(outputPath, exist_ok=True)
logger.info(f"Output directory: {outputPath}.")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Define Paths %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Define group paths for SV, PR and SR Task:
# group_paths = {
#     'HDBaseline': {
#         'SV': {
#             'dataPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Data\SV",
#             'outputPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Features",
#             'figPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Figures\SV"
#         },
#         'PR': {
#             'dataPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Data\PR",
#             'outputPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Features",
#             'figPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Figures\PR"
#         },
#         'SR': {
#             'dataPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Data\SR",
#             'outputPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Features",
#             'figPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Figures\SR"
#         }
#     },
#     'HDFollowUp': {
#         'SV': {
#             'dataPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Data\SV",
#             'outputPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Features",
#             'figPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Figures\SV"
#         },    
#         'PR': {
#             'dataPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Data\PR",
#             'outputPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Features",
#             'figPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Figures\PR"
#         },
#         'SR': {
#             'dataPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Data\SR",
#             'outputPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Features",
#             'figPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Figures\SR"
#         }
#     }
# }

group_paths = {
    'HDFollowUp': {
        'SV': {
            'dataPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Data\SV",
            'outputPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Features",
            'figPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Figures\SV"
        },    
        'PR': {
            'dataPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Data\PR",
            'outputPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Features",
            'figPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Figures\PR"
        },
        'SR': {
            'dataPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Data\SR",
            'outputPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Features",
            'figPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDFollowUp\Figures\SR"
        }
    },
    'HDBaseline': {
        'SV': {
            'dataPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Data\SV",
            'outputPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Features",
            'figPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Figures\SV"
        },
        'PR': {
            'dataPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Data\PR",
            'outputPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Features",
            'figPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Figures\PR"
        },
        'SR': {
            'dataPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Data\SR",
            'outputPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Features",
            'figPath': r"C:\Users\Student\OneDrive - University College Dublin\Desktop\Speech Analysis\Results\Speech Features\groupHDBaseline\Figures\SR"
        }
    }
}

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Define Subtest Names %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Define Subtest Names:
nameSV = ['SV']                                 # SV Task
nameSR = ['SR1', 'SR2', 'SR3', 'SR4', 'SR5']    # Syllable Repetition Task
namePR = ['PR']                                 # Paragraph Reading Task

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Process Groups %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Process Speech Features for each Group (HDBaseline or HDFollowUp) and Test Type (SV, PR or SR):
def process_group(group, test_type, paths):
    logger.info(f"Started processing {group} group for {test_type}...")
    try:
        # Dynamically choose the name list based on test type:
        if test_type == 'SR':
            name_list = nameSR
        elif test_type == 'PR':
            name_list = namePR
        elif test_type == 'SV':
            name_list = nameSV
        
        # Process the speech features using the audioProcessingHDLongitudinal module:
        audioProcessingHDLongitudinal.process_speech_features(
            paths['dataPath'], paths['outputPath'], paths['figPath'], group, name_list
        )
        logger.info(f"Completed processing {group} group for {test_type}.")
    except Exception as e:
        logger.error(f"Error processing {group} group for {test_type}: {e}")
    
    return None

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Process Features %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def process_features(group_paths):
    # Process each group and test type, one by one (HDBaseline and HDFollowUp for SV, PR & SR):
    for group, test_types in group_paths.items():
        for test_type, paths in test_types.items():
            process_group(group, test_type, paths)
    
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Load Processed Features for Analysis %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Load and combine features for each test type:
    for test_type in ['SV', 'SR', 'PR']:
        # Load Baseline Features:
        HDBaselinePath = group_paths['HDBaseline'][test_type]['outputPath']
        try:
            dfHD_Baseline = pd.read_csv(os.path.join(HDBaselinePath, f"features_HDBaseline_{test_type}.csv"))
            dfHD_Baseline.insert(4, 'Group', 'HDBaseline')    # Add Group column to identify as Baseline
            logger.info(f"Successfully loaded HDBaseline {test_type} features.")
        except Exception as e:
            logger.error(f"Error loading HDBaseline {test_type} features: {e}")
            dfHD_Baseline = None                              # Set to None to prevent further errors

        # Load Follow-Up Features:
        HDFollowUpPath = group_paths['HDFollowUp'][test_type]['outputPath']
        try:
            dfHD_Followup = pd.read_csv(os.path.join(HDFollowUpPath, f"features_HDFollowUp_{test_type}.csv"))
            dfHD_Followup.insert(4, 'Group', 'HDFollowUp')   # Add Group column to identify as FollowUp
            logger.info(f"Successfully loaded HDFollowUp {test_type} features.")
        except Exception as e:
            logger.error(f"Error loading HDFollowUp {test_type} features: {e}")
            dfHD_Followup = None                               # Set to None to prevent further errors

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Join Baseline & FollowUp %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # Only attempt to concatenate if both dataframes are loaded correctly:
        if dfHD_Baseline is not None and dfHD_Followup is not None:
            try:
                df = pd.concat([dfHD_Baseline, dfHD_Followup], ignore_index=True)
                
                # Clean up the DataFrame
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')].dropna(axis=1, how='all')
                df = df[df.columns.drop(list(df.filter(regex='pythonVersion')))]
                
                # Save the DataFrame to .csv File & Update the File Path:
                df.to_csv(os.path.join(outputPath, f'Features_HDLongitudinal_{test_type}.csv'), index=False)
                logger.info(f"Successfully saved the combined {test_type} features.")
            except Exception as e:
                logger.error(f"Error processing {test_type} features: {e}")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Main Function %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Ensure multiprocessing is handled: 
if __name__ == '__main__':
    try:
        # Process features for all groups and test types:
        process_features(group_paths)
        logger.info("Processing completed successfully.")
    except Exception as e:
        logger.error(f"Error during processing: {e}", exc_info = True)
    finally:
        # Clean up logging handlers:
        logger.info("Shutting down logging handlers...")
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
