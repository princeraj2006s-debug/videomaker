import streamlit as st
import streamlit.components.v1 as components
from gtts import gTTS
import tempfile
import os
import json
import base64

st.set_page_config(
    page_title="3D Cartoon AI Studio",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #080d1b;
    color: white;
}
h1 {
    color: #65b8ff;
    text-align: center;
}
.stButton button {
    background: linear-gradient(90deg,#1677ff,#8b42ff);
    color: white;
    border-radius: 12px;
    width: 100%;
    height: 50px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 3D CARTOON AI STUDIO")
st.caption("Create interactive 3D animated scenes")

prompt = st.text_area(
    "Describe your 3D cartoon scene",
    "A cute robot walking in a beautiful futuristic city with colorful buildings",
    height=120
)

voice_text = st.text_area(
    "Voiceover Script",
    "Welcome to our amazing cartoon world!"
)

col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "Voice Language",
        ["en", "hi"]
    )

with col2:
    duration = st.slider(
        "Animation Duration",
        5, 30, 10
    )

def detect_objects(text):

    text = text.lower()

    objects = []

    keywords = {
        "robot": "robot",
        "car": "car",
        "dog": "dog",
        "cat": "cat",
        "tree": "tree",
        "house": "house",
        "boy": "person",
        "girl": "person",
        "person": "person",
        "human": "person",
        "elephant": "elephant",
        "dragon": "dragon",
        "ball": "ball",
        "bird": "bird",
        "airplane": "airplane"
    }

    for word, obj in keywords.items():
        if word in text and obj not in objects:
            objects.append(obj)

    if not objects:
        objects = ["robot", "tree"]

    return objects[:5]


def create_scene(objects, prompt):

    scene = {
        "objects": objects,
        "prompt": prompt,
        "duration": duration
    }

    return scene


if st.button("🚀 GENERATE 3D CARTOON"):

    if not prompt.strip():
        st.error("Please enter a prompt.")

    else:

        with st.spinner("Building your 3D scene..."):

            objects = detect_objects(prompt)

            scene = create_scene(
                objects,
                prompt
            )

        st.success("3D Scene Created!")

        # 3D ENGINE

        scene_json = json.dumps(scene)

        html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport"
content="width=device-width, initial-scale=1">

<style>
body {
    margin:0;
    overflow:hidden;
    background:#080d1b;
}
canvas {
    display:block;
}
</style>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js">
</script>
</head>

<body>

<script>

const sceneData = SCENE_DATA;

const scene = new THREE.Scene();

scene.background = new THREE.Color(0x87ceeb);

scene.fog = new THREE.Fog(0x87ceeb, 15, 60);

const camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth/window.innerHeight,
    0.1,
    1000
);

camera.position.set(7,6,12);

const renderer = new THREE.WebGLRenderer({
    antialias:true
});

renderer.setSize(
    window.innerWidth,
    window.innerHeight
);

renderer.setPixelRatio(
    Math.min(window.devicePixelRatio,2)
);

renderer.shadowMap.enabled = true;

document.body.appendChild(renderer.domElement);

// LIGHTS

const ambient = new THREE.AmbientLight(
    0xffffff,
    0.8
);

scene.add(ambient);

const sun = new THREE.DirectionalLight(
    0xffffff,
    2
);

sun.position.set(5,10,5);

sun.castShadow = true;

scene.add(sun);

// GROUND

const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(100,100),
    new THREE.MeshStandardMaterial({
        color:0x42a85a
    })
);

ground.rotation.x = -Math.PI/2;

ground.position.y = -0.1;

ground.receiveShadow = true;

scene.add(ground);

// OBJECT CREATION

const animatedObjects = [];

function material(color) {

    return new THREE.MeshStandardMaterial({
        color:color,
        roughness:0.55,
        metalness:0.05
    });

}

function addMesh(geometry,color,x,y,z){

    const mesh = new THREE.Mesh(
        geometry,
        material(color)
    );

    mesh.position.set(x,y,z);

    mesh.castShadow = true;

    mesh.receiveShadow = true;

    scene.add(mesh);

    return mesh;

}

function createRobot(x){

    const group = new THREE.Group();

    const body = new THREE.Mesh(
        new THREE.BoxGeometry(1.2,1.5,0.8),
        material(0x4287ff)
    );

    body.position.y = 1.5;

    group.add(body);

    const head = new THREE.Mesh(
        new THREE.SphereGeometry(0.65,32,32),
        material(0xe5e8ee)
    );

    head.position.y = 2.7;

    group.add(head);

    const eye1 = addEye(-0.22);
    const eye2 = addEye(0.22);

    head.add(eye1);
    head.add(eye2);

    function addEye(x){

        const eye = new THREE.Mesh(
            new THREE.SphereGeometry(0.09,16,16),
            material(0x111111)
        );

        eye.position.set(x,0.05,0.58);

        return eye;

    }

    group.position.x = x;

    scene.add(group);

    animatedObjects.push(group);

}

function createPerson(x){

    const group = new THREE.Group();

    const body = new THREE.Mesh(
        new THREE.CapsuleGeometry(0.4,0.9,4,12),
        material(0x2563eb)
    );

    body.position.y = 1.2;

    group.add(body);

    const head = new THREE.Mesh(
        new THREE.SphereGeometry(0.42,32,32),
        material(0xffc99c)
    );

    head.position.y = 2.15;

    group.add(head);

    group.position.x = x;

    scene.add(group);

    animatedObjects.push(group);

}

function createTree(x){

    addMesh(
        new THREE.CylinderGeometry(0.25,0.4,2,12),
        0x784421,
        x,1,0
    );

    addMesh(
        new THREE.SphereGeometry(1.3,24,24),
        0x078b42,
        x,2.5,0
    );

}

function createCar(x){

    const group = new THREE.Group();

    const body = new THREE.Mesh(
        new THREE.BoxGeometry(2,0.7,1),
        material(0xff3333)
    );

    body.position.y = 0.7;

    group.add(body);

    const roof = new THREE.Mesh(
        new THREE.BoxGeometry(1,0.6,0.8),
        material(0xffcc22)
    );

    roof.position.y = 1.3;

    group.add(roof);

    for(let i=0;i<4;i++){

        const wheel = new THREE.Mesh(
            new THREE.CylinderGeometry(
                0.25,0.25,0.15,20
            ),
            material(0x222222)
        );

        wheel.rotation.z = Math.PI/2;

        wheel.position.set(
            i<2 ? -0.65:0.65,
            0.35,
            i%2===0 ? 0.55:-0.55
        );

        group.add(wheel);

    }

    group.position.x = x;

    scene.add(group);

    animatedObjects.push(group);

}

function createElephant(x){

    const group = new THREE.Group();

    const body = new THREE.Mesh(
        new THREE.SphereGeometry(0.9,32,32),
        material(0x9999aa)
    );

    body.scale.set(1.3,0.85,0.9);

    body.position.y = 1.1;

    group.add(body);

    const head = new THREE.Mesh(
        new THREE.SphereGeometry(0.6,32,32),
        material(0xaaaaBB)
    );

    head.position.set(0.8,1.7,0);

    group.add(head);

    group.position.x = x;

    scene.add(group);

    animatedObjects.push(group);

}

function createAnimal(x,type){

    const group = new THREE.Group();

    const body = new THREE.Mesh(
        new THREE.SphereGeometry(0.7,24,24),
        material(type==="cat" ? 0xffaa44:0x996633)
    );

    body.position.y=0.8;

    group.add(body);

    const head = new THREE.Mesh(
        new THREE.SphereGeometry(0.5,24,24),
        material(type==="cat" ? 0xffaa44:0x996633)
    );

    head.position.set(0.65,1.2,0);

    group.add(head);

    group.position.x=x;

    scene.add(group);

    animatedObjects.push(group);

}

function createDragon(x){

    const group = new THREE.Group();

    const body = new THREE.Mesh(
        new THREE.SphereGeometry(0.9,24,24),
        material(0x27a65a)
    );

    body.position.y=1.4;

    group.add(body);

    const head = new THREE.Mesh(
        new THREE.SphereGeometry(0.55,24,24),
        material(0x35cc77)
    );

    head.position.set(0.8,1.8,0);

    group.add(head);

    group.position.x=x;

    scene.add(group);

    animatedObjects.push(group);

}

// CREATE PROMPT OBJECTS

const spacing = 3;

sceneData.objects.forEach((type,index)=>{

    const x = (
        index-(sceneData.objects.length-1)/2
    )*spacing;

    if(type==="robot") createRobot(x);

    if(type==="person") createPerson(x);

    if(type==="tree") createTree(x);

    if(type==="car") createCar(x);

    if(type==="elephant") createElephant(x);

    if(type==="dog" || type==="cat")
        createAnimal(x,type);

    if(type==="dragon") createDragon(x);

    if(type==="bird") {

        addMesh(
            new THREE.SphereGeometry(0.4,20,20),
            0xffcc22,x,3,0
        );

    }

    if(type==="ball") {

        const ball = addMesh(
            new THREE.SphereGeometry(0.7,32,32),
            0xff2222,x,1,0
        );

        animatedObjects.push(ball);

    }

    if(type==="house") {

        addMesh(
            new THREE.BoxGeometry(2,2,2),
            0xffcc88,x,1,0
        );

        addMesh(
            new THREE.ConeGeometry(1.6,1.2,4),
            0xaa3333,x,2.6,0
        );

    }

    if(type==="airplane") {

        addMesh(
            new THREE.BoxGeometry(3,0.25,0.4),
            0xffffff,x,4,0
        );

    }

});

// CAMERA

let time = 0;

function animate(){

    requestAnimationFrame(animate);

    time += 0.015;

    animatedObjects.forEach((obj,index)=>{

        obj.position.y +=
            Math.sin(time*2+index)*0.003;

        obj.rotation.y =
            Math.sin(time+index)*0.15;

    });

    camera.position.x =
        Math.sin(time*0.25)*2;

    camera.lookAt(0,1,0);

    renderer.render(scene,camera);

}

animate();

window.addEventListener("resize",()=>{

    camera.aspect =
        window.innerWidth/window.innerHeight;

    camera.updateProjectionMatrix();

    renderer.setSize(
        window.innerWidth,
        window.innerHeight
    );

});

</script>

</body>
</html>
"""

        html = html.replace(
            "SCENE_DATA",
            scene_json
        )

        st.subheader("🎥 Your 3D Cartoon Preview")

        components.html(
            html,
            height=500,
            scrolling=False
        )

        # VOICE GENERATION

        if voice_text.strip():

            with st.spinner("Generating voiceover..."):

                try:

                    with tempfile.NamedTemporaryFile(
                        suffix=".mp3",
                        delete=False
                    ) as temp:

                        audio_path = temp.name

                    tts = gTTS(
                        text=voice_text,
                        lang=language
                    )

                    tts.save(audio_path)

                    with open(audio_path,"rb") as f:

                        st.audio(
                            f.read(),
                            format="audio/mp3"
                        )

                        st.download_button(
                            "📥 Download Voiceover",
                            f.read(),
                            file_name="voiceover.mp3",
                            mime="audio/mp3"
                        )

                    os.remove(audio_path)

                except Exception as e:

                    st.warning(
                        f"Voice error: {e}"
                    )

st.markdown("---")

st.caption(
    "3D Cartoon Studio | Three.js + Streamlit + gTTS"
)
