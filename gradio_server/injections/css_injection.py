css_injection = """
#component-25 {min-width: min(1000px, 100%) !important} 
footer {visibility: hidden} 
#video_in > * > button[aria-label="Clear"] {visibility: hidden} 
div.button-wrap { visibility: hidden; } 
.contain > div > div > div > div {flex-grow: 0 !important;} 
.fullscreen-enabled {
    position: fixed; /* Fixed positioning relative to the viewport */
    top: 0;
    left: 10%;
    object-fit: contain; /* Ensures the content is completely visible */
    width: 80%;
    height: 100%;
    background-color: #0b0f19;
    z-index: 1000; /* High z-index to ensure it's on top */
}
label[data-testid="block-label"] svg.feather-video {
    display: none;
}
label[data-testid="block-label"]:has(svg.feather-video) {
    display: none;
}
.fullscreen-button {
    position: absolute;
    top: 2em;
    right: 10px;
    z-index: 10000;
}"""