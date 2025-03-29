import os

def setup():

    os.environ["POLICY_PIPELINE_CONFIG_FILE_PATH"] = ""

    os.environ["PASSWORD_U_POLICY_PIPELINE_ACCOUNT1"] = "MY_PASSWORD_1"
    os.environ["PASSWORD_U_POLICY_PIPELINE_ACCOUNT2"] = "MY_PASSWORD_2"
    os.environ["PASSWORD_U_POLICY_PIPELINE_ACCOUNT3_PROJECT1"] = "MY_PASSWORD_3"
    os.environ["PASSWORD_U_POLICY_PIPELINE_ACCOUNT3_PROJECT2"] = "MY_PASSWORD_4"

if __name__ == "__main__":
    setup()