import argparse
import torch
import json
from model import CustomResNet
from  monai.networks.nets import DenseNet121
    
from monai.transforms import (
    Compose,
    LoadImage,
    EnsureType,
    ToTensor,
    EnsureChannelFirst,
    DivisiblePad,
    Orientation,
    NormalizeIntensity,
    )


def load_model(model, weight_file, device='cpu'):
    weights = torch.load(weight_file, map_location=device, weights_only=True)
    new_weights = {key.replace('module.', ''): value for key, value in weights.items()}
    model.load_state_dict(new_weights)
    model.to(device)
    return model


def inference(subject_id, left, right, mri_2mm):
    gca_weight_file = 'models/gca_model.pth'
    mta_weight_file = 'models/mta_model.pth'
    erica_weight_file = 'models/erica_model.pth'
    cls_weight_file = 'models/cls_model.pth'


    val_transforms = Compose(
        [
            LoadImage(reader='NibabelReader'),
            EnsureChannelFirst(),
            EnsureType(),
            Orientation(as_closest_canonical=True),
            DivisiblePad(k=32),
            NormalizeIntensity(subtrahend=0, divisor=255),
            ToTensor(dtype=torch.float32),
        ]
    )

    left_tensor = val_transforms(left).unsqueeze(0)
    right_tensor = val_transforms(right).unsqueeze(0)
    mri_tensor = val_transforms(mri_2mm).unsqueeze(0)

    # print(left_tensor.shape)
    # print(right_tensor.shape)
    # print(mri_tensor.shape)

    cls_model = DenseNet121(spatial_dims=3, in_channels=1, out_channels=3, init_features=64, growth_rate=32, block_config=(6, 12, 24, 16), pretrained=False, progress=True)
    gca_model = CustomResNet(num_classes=4)
    mta_model = CustomResNet(num_classes=5)
    erica_model = CustomResNet(num_classes=4)
    # # # print(model.state_dict())
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    cls_model.to(device)
    gca_model.to(device)
    mta_model.to(device)
    erica_model.to(device)
    
    # cls_preds = []
    # gca_preds = []
    # mta_right_preds = []
    # mta_left_preds = []
    # erica_right_preds = []
    # erica_left_preds = []

    # # # Load the original state dictionary from a checkpoint file
    load_model(cls_model, cls_weight_file, device)
    load_model(gca_model, gca_weight_file, device)
    load_model(mta_model, mta_weight_file, device)
    load_model(erica_model, erica_weight_file, device)

    cls_model.eval()
    gca_model.eval()
    mta_model.eval()
    erica_model.eval()

    with torch.no_grad():

        print("Predicting classes... ")
        gca = mri_tensor.to(device)
        right_path = right_tensor.to(device)
        left_path = left_tensor.to(device)

        cls_logits = cls_model(gca)
        gca_logits = gca_model(gca)
        mta_right_logits = mta_model(right_path)
        mta_left_logits = mta_model(left_path)
        erica_right_logits = erica_model(right_path)
        erica_left_logits = erica_model(left_path)

        # cls_preds.extend([dx for cls in cls_pred for dx in cls])
        # gca_preds.extend(gca_pred)
        # mta_right_preds.extend(mta_right_pred)
        # mta_left_preds.extend(mta_left_pred)
        # erica_right_preds.extend(erica_right_pred)
        # erica_left_preds.extend(erica_left_pred)

        cls_conf, cls_pred = torch.max(torch.softmax(cls_logits, 1), 1)
        gca_conf, gca_pred = torch.max(torch.softmax(gca_logits, 1), 1)
        mta_right_conf, mta_right_pred = torch.max(torch.softmax(mta_right_logits, 1), 1)
        mta_left_conf, mta_left_pred = torch.max(torch.softmax(mta_left_logits, 1), 1)
        erica_right_conf, erica_right_pred = torch.max(torch.softmax(erica_right_logits, 1), 1)
        erica_left_conf, erica_left_pred = torch.max(torch.softmax(erica_left_logits, 1), 1)

        diagnosis_map = {0: "Normal", 1: "Mild Cognitive Impairment", 2: "Alzheimer's Disease"}

        print("Prediction Result: ", "AI DX: ", cls_pred.item(),
                "GCA: ", gca_pred.item(), 
                "MTA_RIGHT: ", mta_right_pred.item(), "MTA_LEFT: ", mta_left_pred.item(),
                "ERICA_RIGHT: ", erica_right_pred.item(), "ERICA_LEFT: ", erica_left_pred.item())
        
        predictions = {
                       "Subject_id": subject_id,
                       "Diagnosis": diagnosis_map[cls_pred.item()],
                       "Diagnosis_conf": round(cls_conf.item()*100, 2),
                       "GCA": gca_pred.item(),
                       "GCA_conf": round(gca_conf.item()*100, 2),
                       "MTA_RIGHT": mta_right_pred.item(),
                       "MTA_RIGHT_conf": round(mta_right_conf.item()*100, 2),
                       "MTA_LEFT": mta_left_pred.item(),
                       "MTA_LEFT_conf": round(mta_left_conf.item()*100, 2),
                       "ERICA_RIGHT": erica_right_pred.item(),
                       "ERICA_RIGHT_conf": round(erica_right_conf.item()*100, 2),
                       "ERICA_LEFT": erica_left_pred.item(),
                       "ERICA_LEFT_conf": round(erica_left_conf.item()*100, 2)}
        
        filename = f"results/{subject_id}/predictions.json"
        with open(filename, 'w') as file:
            json.dump(predictions, file, indent=4)

    # prediction_df = pd.concat([df, prediction_df], axis=1)
    # prediction_df.to_csv(save_file, index=False)

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Registered transform using the transformation matrix.")
    parser.add_argument('-s', '--subject_id', type=str, required=True, help='Subject ID')

    args = parser.parse_args()
    subject_id = args.subject_id  
    left = f'results/{subject_id}/cropped/norm_to_mni305_1mm_left.nii.gz'
    right = f'results/{subject_id}/cropped/norm_to_mni305_1mm_right.nii.gz'
    mri_2mm = f'results/{subject_id}/norm_to_mni305_2mm.nii.gz'

    inference(subject_id, left, right, mri_2mm)
