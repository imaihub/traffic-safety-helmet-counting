import gradio as gr


def check_model_settings(model_manager):
    if not model_manager.model_settings.architecture or not model_manager.model_settings.weights_path:
        model_manager.logger.warn("Input present but no model, tracker or weights")
        gr.Warning("Input present but no model, tracker or weights")
        return None
    return True
