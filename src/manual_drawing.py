import nibabel as nib
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TKAgg')
import argparse


def show_slices(slices, img, path):
    # Function to display rows of image slices
    fig, axes = plt.subplots(4, 2)
    fig.set_figheight(16), fig.set_figwidth(10)
    
    titles = ['Coronal Mid Front', 'Sagittal Mid Right', 'Coronal Mid Back', 'Sagittal Mid Left',  'Axial Mid', 'Sagittal Right', 'Axial Lower', 'Sagittal Left']

    for i in range(4):  # Loop over 4 rows
        for j in range(2):  # Loop over 2 columns
            index = i * 2 + j  # Calculate index for accessing the slices
            if index < len(slices):
                ax = axes[i, j]
                ax.imshow(slices[index].T, cmap="gray", origin="lower")
                
                # Set the grid
                ax.grid(which='major', color='#DDDDDD', linewidth=0.5)
                ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.3)
                ax.minorticks_on()
                
                # Set tick labels font size
                ax.tick_params(axis='both', which='major', labelsize=6)
                ax.tick_params(axis='both', which='minor', labelsize=6)

                # Set title at the bottom of the subplot
                ax.set_title(titles[index], fontsize=8, loc='center', pad=-15)  # Adjust pad as needed

            else:
                ax.axis('off')  # Hide unused axes

    # Save the figure
    fig.savefig(path, dpi=300, bbox_inches='tight')
    # plt.show()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Registered transform using the transformation matrix.")
    parser.add_argument('-s', '--subject_id', type=str, required=True, help='Subject ID')

    args = parser.parse_args()    

    subject_id = args.subject_id
    path = f'results/{subject_id}/norm_to_mni305_1mm.nii.gz'

    img = nib.load(path)
    img = nib.as_closest_canonical(img)
    print("Image shape: ", img.shape)
    # OrthoSlicer3D(img.get_fdata()).show()

    x = img.get_fdata()
    x_shape = x.shape

    d1 = int(x_shape[0]/4 + 5)
    d2 = int(x_shape[0]/2 + 8)
    d3 = int(x_shape[2]/2 + 0)
    d4 = int(x_shape[0] - x_shape[0]/4 - 5)
    d5 = int(x_shape[1]/2 - 5)
    d6 = int(x_shape[2]/3 + 0)

    d7 = int(x_shape[0]/2 - 8)
    d8 = int(x_shape[1]/2 + 5)


    slice_0 = x[:, d8, :]
    slice_1 = x[d2, :, :]
    slice_2 = x[:, d5, :]
    slice_3 = x[d7, :, :]
    slice_4 = x[:, :, d3]
    slice_5 = x[d4, :, :]
    slice_6 = x[:, :, d6]
    slice_7 = x[d1, :, :]
    

    slices = [slice_0, slice_1, slice_2, slice_3, slice_4, slice_5, slice_6, slice_7]
    save_path = f'results/{subject_id}/image_slices.jpg'
    show_slices(slices, img, save_path)
