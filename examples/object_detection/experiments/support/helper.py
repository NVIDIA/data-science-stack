import torch
from determined.experimental import Determined
from .data import load_and_transform_image, draw_example

def predict(experiment_id, file, det_master=None):

    if det_master:
        checkpoint = Determined(master=det_master).get_experiment(experiment_id).top_checkpoint()
    else:
        checkpoint = Determined().get_experiment(experiment_id).top_checkpoint()

    model = checkpoint.load().model

    run_predict(model, file)


def filter_boxes(boxes, scores, threshold):
    cutoff = 0
    for i, score in enumerate(scores):
        if score < threshold:
            break
        cutoff = i
    # slicing excludes end, so we add 1 in the general case, and set to None if all
    # boxes are to be returned
    cutoff = None if cutoff == len(scores) - 1 else cutoff + 1
    return boxes[:cutoff]


def run_predict(model, file, threshold=0.7):
    model.eval()
    test_image = load_and_transform_image(file)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if torch.cuda.is_available():
        model.cuda()

    with torch.no_grad():
        outputs = model(test_image.unsqueeze(0).to(device))[0]

    if len(outputs['boxes']) > 0:
        boxes = filter_boxes(outputs['boxes'], outputs['scores'], threshold)
        draw_example(test_image.permute(1,2,0).cpu().numpy(), {'boxes': boxes.cpu()}, title="Predictions")
    else:
        print("No objects detected!")