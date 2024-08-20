from promptflow.core import Prompty, AzureOpenAIModelConfiguration
import json
import os 
from dotenv import load_dotenv 
from pathlib import Path
folder = Path(__file__).parent.absolute().as_posix()


load_dotenv()

def edit(article, feedback):
    
    # Load prompty with AzureOpenAIModelConfiguration override
    configuration = AzureOpenAIModelConfiguration(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=f"https://{os.getenv('AZURE_OPENAI_NAME')}.cognitiveservices.azure.com/"
    )
    override_model = {
        "configuration": configuration,
        "parameters": {"max_tokens": 512}
    }
    # create path to prompty file
    path_to_prompty = folder + "/editor.prompty"

    prompty_obj = Prompty.load(path_to_prompty, model=override_model)
    result = prompty_obj(article=article, feedback=feedback,)
    
    return result


if __name__ == "__main__":

    result = edit(
        "Satya Nadella: A Symphony of Education and Innovation\n\nIn a world constantly reshaped by technology, Satya Nadella stands as a testament to the power of education as a launching pad for innovative leadership. Born on August 19, 1967, in Hyderabad, India, Nadella's journey from a middle-class family to the helm of Microsoft is a narrative of persistence, intellectual curiosity, and the transformative influence of education.\n\nThe formative phase of Nadella's education took root at the Hyderabad Public School, Begumpet, where he cultivated a passion for learning and a clear intellectual aptitude [Citation](https://www.educba.com/satya-nadella-biography/). This academic foundation soon spread its branches outward, reaching the Manipal Institute of Technology in Karnataka, India, where Nadella earned a bachelor's degree in electrical engineering in 1988 [Citation](https://en.wikipedia.org/wiki/Satya_Nadella).\n\nHowever, the essence of Nadella's educational prowess lies not merely in the degrees obtained but in his unwavering zeal for knowledge which propelled him across oceans. Post his undergraduate studies, Nadella pursued a Master's degree in Computer Science from the University of Wisconsin-Milwaukee and further, an MBA from the University of Chicago. This diverse educational landscape equipped him with a robust technical expertise, a strategic business acumen, and a global perspective—cornerstones of his leadership philosophy at Microsoft.\n\nNadella's educational journey emerges as a beacon of his career trajectory, exemplified in his ascension to becoming the executive vice president of Microsoft's cloud and enterprise group, and ultimately the CEO and Chairman of Microsoft [Citation](https://www.britannica.com/biography/Satya-Nadella). His leadership is a continual echo of his learnings, emphasizing the importance of continuous growth and the potential of technology to empower people and organizations across the globe.\n\nIn conclusion, the educational odyssey of Satya Nadella illuminates his career at Microsoft and beyond, underscoring the necessity of a strong educational foundation in molding the leaders who shape our digital futures.",
        "Research Feedback:\nAdditional specifics on how each phase of his education directly influenced particular career decisions or leadership styles at Microsoft would enhance the narrative. Information on key projects or initiatives that Nadella led, correlating to his expertise gained from his various degrees, would add depth to the discussion on the interplay between his education and career milestones.",
    )
    # parse string to json
    result = json.loads(result)
    print(result)