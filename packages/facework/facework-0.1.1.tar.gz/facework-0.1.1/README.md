# FaceWork

**FaceWork** is a user-friendly Python library that helps you **crop faces** and create **face morphing animations** from images. Whether you're working on a creative project or doing face-related image processing, FaceWork makes it simple and efficient.

---

## ✨ Features

- **FaceCrop**: Automatically detects and crops a face from an image (image must contain one face only).
- **FaceMorph**: Morph two face images into a smooth transition (image sequence or video).

---

## 🔧 Installation

Before installing FaceWork, you’ll need two external tools:

### 1. Install ImageMagick (Required)

Download and install ImageMagick from the official website:

👉 [https://imagemagick.org/script/download.php](https://imagemagick.org/script/download.php)

Make sure to choose the right version for your operating system.

---

### 2. Install FFmpeg (Optional, only for video output)

If you want to create videos using `FaceMorph.make_morph_video()`, you'll also need **FFmpeg**:

👉 [https://www.ffmpeg.org/download.html](https://www.ffmpeg.org/download.html)

#### Recommended Steps (for Windows users):
1. Download a static build from the **"Get packages & executable files"** section.
2. Unzip the folder and move it to `C:\Program Files\ffmpeg` (or any other location you prefer).
3. Inside the `ffmpeg` folder, open the `bin` directory and copy its path.
4. Add that path to your system’s **Environment Variables**:
   - Open the Start menu and search for **Environment Variables**.
   - Click **Edit the system environment variables** > **Environment Variables**.
   - Under **System Variables**, find and select `Path`, click **Edit**, then **New**, and paste the path to the `bin` folder.
   - Save and close.

---

### 3. Install FaceWork

Once the dependencies are ready, install FaceWork via pip:

```bash
pip install facework
```

---

## 🚀 Usage

FaceWork provides two main classes: `FaceCrop` and `FaceMorph`.

### 🔲 FaceCrop

`FaceCrop` detects and crops the face from an image. It's ideal for focusing on facial regions for further analysis or processing.

- **Input**: An image containing a single face.
- **Output**: A cropped version of the image, centered on the face.
- **Note**: The input image must contain **only one face**.

➡️ Example usage:  
See `examples/example_FaceCrop.py` for a practical demonstration.

---

### 🔁 FaceMorph

`FaceMorph` creates a smooth morphing transition between two faces. It can generate either:

- A **sequence of images**, showing gradual transformation.
- An **MP4 video** (requires FFmpeg), animating the morphing process.

- **Input**: Two images, each containing one face.
- **Best results**: Use frontal, eye-level photographs with similar lighting.
- **Output**: A list of transitional images or a video file.
- The transition is linear—each frame represents an equal percentage shift toward the second face.

➡️ Example usage:  
See `examples/example_FaceMorph.py` for a working example.

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 📦 Third-party Licenses

This project includes and depends on the following third-party libraries and tools. Each is governed by its own license terms as listed below:

---

### 🖼️ [ImageMagick](https://imagemagick.org)

Licensed under the [ImageMagick License](https://imagemagick.org/script/license.php).  
Copyright © 2025  
Distributed "AS IS", without warranties or conditions of any kind.

---

### 🎞️ [FFmpeg](https://ffmpeg.org)

This software uses components of the FFmpeg project under the **LGPLv2.1** license.  
The FaceWork project does **not** own FFmpeg.

---

### 📼 python-ffmpeg

Licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)  
© 2017 Karl Kroening

---

### 🔍 MediaPipe

Licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)  


---

### 🎥 OpenCV (opencv-python)

Licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)

---

### 🧮 NumPy

Licensed under a BSD-style license.  
© 2005–2024 NumPy Developers  
Redistribution and use permitted under certain conditions.  
See full license in the NumPy documentation.

---

### 📊 Pandas

Licensed under the [BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause)  
© 2008–2011 AQR Capital Management, LLC, Lambda Foundry, Inc., PyData Development Team  
© 2011–2025 Open Source Contributors

---

### 🔬 SciPy

Licensed under the [BSD License](https://opensource.org/licenses/BSD-3-Clause)  
© 2001–2002 Enthought, Inc.  
© 2003–present SciPy Developers

---

### 🪄 Wand (Python bindings for ImageMagick)

Licensed under the MIT License.  
Original work © 2011–2018 Hong Minhee  
Modified work © 2019–2025 E. McConville

---

### 📈 Matplotlib

Licensed under the Matplotlib License:

- Versions ≥1.3.0: © 2012–present Matplotlib Development Team
- Versions <1.3.0: © 2002–2011 John D. Hunter

See details at [Matplotlib Licensing](https://matplotlib.org/stable/users/project/license.html)

---

### 🖼️ Pillow (PIL Fork)

Licensed under the MIT-CMU License  
- PIL: © 1995–2011 Fredrik Lundh and contributors  
- Pillow: © 2010–present Jeffrey A. Clark and contributors

---

### ⚙️ psutil

Licensed under the [BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause)  
© 2009 Jay Loden, Dave Daeschler, Giampaolo Rodola

---

Please refer to each library's official documentation or LICENSE file for the full terms.
