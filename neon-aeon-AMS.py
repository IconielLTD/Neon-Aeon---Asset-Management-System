import customtkinter as ctk
import json
from tkinter import filedialog, messagebox
from typing import Dict, List, Any

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NeonAeonManager:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Neon Aeon - Asset Manager")
        self.root.geometry("1400x900")
        
        self.project = {
            "name": "Neon Aeon Project",
            "acts": []
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = ctk.CTkFrame(self.root)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        self.project_name = ctk.CTkEntry(
            header_frame, 
            placeholder_text="Project Name",
            font=("Arial", 24, "bold"),
            height=50
        )
        self.project_name.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.project_name.insert(0, self.project["name"])
        
        btn_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(
            btn_frame,
            text="Import",
            command=self.import_project,
            width=100
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Export JSON",
            command=self.export_project,
            fg_color="green",
            hover_color="darkgreen",
            width=100
        ).pack(side="left", padx=5)
        
        # Main content with scrollbar
        self.main_frame = ctk.CTkScrollableFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Add Act button
        ctk.CTkButton(
            self.root,
            text="+ Add Act",
            command=self.add_act,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="purple",
            hover_color="darkviolet"
        ).pack(fill="x", padx=20, pady=(0, 20))
        
        self.refresh_ui()
    
    def refresh_ui(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Rebuild acts
        for act_idx, act in enumerate(self.project["acts"]):
            self.create_act_widget(act_idx, act)
    
    def create_act_widget(self, act_idx: int, act: Dict):
        act_frame = ctk.CTkFrame(self.main_frame)
        act_frame.pack(fill="x", pady=5)
        
        # Act header
        act_header = ctk.CTkFrame(act_frame)
        act_header.pack(fill="x", padx=10, pady=10)
        
        act_name = ctk.CTkEntry(act_header, placeholder_text="Act Name", font=("Arial", 16, "bold"))
        act_name.pack(side="left", fill="x", expand=True, padx=(0, 10))
        act_name.insert(0, act["name"])
        act_name.bind("<KeyRelease>", lambda e: self.update_act_name(act_idx, act_name.get()))
        
        ctk.CTkButton(
            act_header,
            text="+ Scene",
            command=lambda: self.add_scene(act_idx),
            width=100,
            fg_color="purple"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            act_header,
            text="Delete Act",
            command=lambda: self.delete_act(act_idx),
            width=100,
            fg_color="red",
            hover_color="darkred"
        ).pack(side="left", padx=5)
        
        # Scenes
        for scene_idx, scene in enumerate(act["scenes"]):
            self.create_scene_widget(act_frame, act_idx, scene_idx, scene)
    
    def create_scene_widget(self, parent, act_idx: int, scene_idx: int, scene: Dict):
        scene_frame = ctk.CTkFrame(parent, fg_color=("#3a3a3a", "#2a2a2a"))
        scene_frame.pack(fill="x", padx=20, pady=5)
        
        # Scene header
        scene_header = ctk.CTkFrame(scene_frame, fg_color="transparent")
        scene_header.pack(fill="x", padx=10, pady=10)
        
        scene_name = ctk.CTkEntry(scene_header, placeholder_text="Scene Name", font=("Arial", 14, "bold"))
        scene_name.pack(side="left", fill="x", expand=True, padx=(0, 10))
        scene_name.insert(0, scene["name"])
        scene_name.bind("<KeyRelease>", lambda e: self.update_scene_name(act_idx, scene_idx, scene_name.get()))
        
        ctk.CTkButton(
            scene_header,
            text="+ Video Node",
            command=lambda: self.add_node(act_idx, scene_idx, "video"),
            width=120,
            fg_color="blue"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            scene_header,
            text="+ Image Node",
            command=lambda: self.add_node(act_idx, scene_idx, "dialogue"),
            width=120,
            fg_color="green"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            scene_header,
            text="+ Audio Track",
            command=lambda: self.add_audio_track(act_idx, scene_idx),
            width=120,
            fg_color="orange"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            scene_header,
            text="Delete",
            command=lambda: self.delete_scene(act_idx, scene_idx),
            width=80,
            fg_color="red"
        ).pack(side="left", padx=2)
        
        # Audio tracks
        if "audioTracks" in scene and scene["audioTracks"]:
            audio_frame = ctk.CTkFrame(scene_frame, fg_color="transparent")
            audio_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(audio_frame, text="🎵 Audio Tracks:", font=("Arial", 12)).pack(anchor="w", pady=(0, 5))
            
            for track_idx, track in enumerate(scene["audioTracks"]):
                self.create_audio_track_widget(audio_frame, act_idx, scene_idx, track_idx, track)
        
        # Nodes
        for node_idx, node in enumerate(scene["nodes"]):
            self.create_node_widget(scene_frame, act_idx, scene_idx, node_idx, node)
    
    def create_audio_track_widget(self, parent, act_idx: int, scene_idx: int, track_idx: int, track: Dict):
        track_frame = ctk.CTkFrame(parent)
        track_frame.pack(fill="x", padx=20, pady=2)
        
        label_entry = ctk.CTkEntry(track_frame, placeholder_text="Label (BGM, SFX, etc)", width=150)
        label_entry.pack(side="left", padx=5)
        label_entry.insert(0, track.get("label", ""))
        label_entry.bind("<KeyRelease>", lambda e: self.update_audio_track(act_idx, scene_idx, track_idx, "label", label_entry.get()))
        
        path_entry = ctk.CTkEntry(track_frame, placeholder_text="Audio file path")
        path_entry.pack(side="left", fill="x", expand=True, padx=5)
        path_entry.insert(0, track.get("path", ""))
        path_entry.bind("<KeyRelease>", lambda e: self.update_audio_track(act_idx, scene_idx, track_idx, "path", path_entry.get()))
        
        ctk.CTkButton(
            track_frame,
            text="Browse",
            command=lambda: self.browse_file(path_entry),
            width=80
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            track_frame,
            text="X",
            command=lambda: self.delete_audio_track(act_idx, scene_idx, track_idx),
            width=40,
            fg_color="red"
        ).pack(side="left", padx=5)
    
    def create_node_widget(self, parent, act_idx: int, scene_idx: int, node_idx: int, node: Dict):
        node_frame = ctk.CTkFrame(parent, fg_color=("#2a2a2a", "#1a1a1a"))
        node_frame.pack(fill="x", padx=20, pady=5)
        
        # Node header
        node_header = ctk.CTkFrame(node_frame, fg_color="transparent")
        node_header.pack(fill="x", padx=10, pady=10)
        
        node_type_label = ctk.CTkLabel(
            node_header, 
            text="VIDEO" if node["type"] == "video" else "IMAGE",
            fg_color="blue" if node["type"] == "video" else "green",
            corner_radius=5,
            width=80,
            font=("Arial", 10, "bold")
        )
        node_type_label.pack(side="left", padx=(0, 10))
        
        # Display node ID
        node_id_label = ctk.CTkLabel(
            node_header,
            text=f"ID: {node['id']}",
            font=("Arial", 9),
            text_color="gray"
        )
        node_id_label.pack(side="left", padx=(0, 10))
        
        node_name = ctk.CTkEntry(node_header, placeholder_text="Node Name")
        node_name.pack(side="left", fill="x", expand=True, padx=(0, 10))
        node_name.insert(0, node["name"])
        node_name.bind("<KeyRelease>", lambda e: self.update_node_name(act_idx, scene_idx, node_idx, node_name.get()))
        
        ctk.CTkButton(
            node_header,
            text="+ Choice",
            command=lambda: self.add_choice(act_idx, scene_idx, node_idx),
            width=100,
            fg_color="orange"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            node_header,
            text="Delete",
            command=lambda: self.delete_node(act_idx, scene_idx, node_idx),
            width=80,
            fg_color="red"
        ).pack(side="left", padx=5)
        
        # Node content
        content_frame = ctk.CTkFrame(node_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        if node["type"] == "video":
            self.create_video_node_fields(content_frame, act_idx, scene_idx, node_idx, node)
        else:
            self.create_dialogue_node_fields(content_frame, act_idx, scene_idx, node_idx, node)
        
        # Choices
        if "choices" in node and node["choices"]:
            choices_frame = ctk.CTkFrame(node_frame, fg_color="transparent")
            choices_frame.pack(fill="x", padx=10, pady=(0, 10))
            
            ctk.CTkLabel(choices_frame, text="Choices:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
            
            for choice_idx, choice in enumerate(node["choices"]):
                self.create_choice_widget(choices_frame, act_idx, scene_idx, node_idx, choice_idx, choice)
    
    def create_video_node_fields(self, parent, act_idx: int, scene_idx: int, node_idx: int, node: Dict):
        video_frame = ctk.CTkFrame(parent, fg_color="transparent")
        video_frame.pack(fill="x", pady=2)
        
        video_entry = ctk.CTkEntry(video_frame, placeholder_text="Video file path")
        video_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        video_entry.insert(0, node.get("videoPath", ""))
        video_entry.bind("<KeyRelease>", lambda e: self.update_node_field(act_idx, scene_idx, node_idx, "videoPath", video_entry.get()))
        
        ctk.CTkButton(
            video_frame,
            text="Browse",
            command=lambda: self.browse_file_for_entry(video_entry, act_idx, scene_idx, node_idx, "videoPath"),
            width=80
        ).pack(side="left")
        
        text_box = ctk.CTkTextbox(parent, height=60)
        text_box.pack(fill="x", pady=2)
        
        # Add placeholder text if empty
        current_text = node.get("dialogueText", "")
        if current_text:
            text_box.insert("1.0", current_text)
        else:
            text_box.insert("1.0", "Dialogue text here...")
            text_box.configure(text_color="gray")
        
        def on_focus_in(event):
            if text_box.get("1.0", "end-1c") == "Dialogue text here...":
                text_box.delete("1.0", "end")
                text_box.configure(text_color="white")
        
        def on_focus_out(event):
            if not text_box.get("1.0", "end-1c").strip():
                text_box.insert("1.0", "Dialogue text here...")
                text_box.configure(text_color="gray")
        
        def on_key_release(event):
            text = text_box.get("1.0", "end-1c")
            if text != "Dialogue text here...":
                self.update_node_field(act_idx, scene_idx, node_idx, "dialogueText", text)
        
        text_box.bind("<FocusIn>", on_focus_in)
        text_box.bind("<FocusOut>", on_focus_out)
        text_box.bind("<KeyRelease>", on_key_release)
    
    def create_dialogue_node_fields(self, parent, act_idx: int, scene_idx: int, node_idx: int, node: Dict):
        image_frame = ctk.CTkFrame(parent, fg_color="transparent")
        image_frame.pack(fill="x", pady=2)
        
        image_entry = ctk.CTkEntry(image_frame, placeholder_text="Image file path")
        image_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        image_entry.insert(0, node.get("imagePath", ""))
        image_entry.bind("<KeyRelease>", lambda e: self.update_node_field(act_idx, scene_idx, node_idx, "imagePath", image_entry.get()))
        
        ctk.CTkButton(
            image_frame,
            text="Browse",
            command=lambda: self.browse_file_for_entry(image_entry, act_idx, scene_idx, node_idx, "imagePath"),
            width=80
        ).pack(side="left")
        
        audio_frame = ctk.CTkFrame(parent, fg_color="transparent")
        audio_frame.pack(fill="x", pady=2)
        
        audio_entry = ctk.CTkEntry(audio_frame, placeholder_text="Dialogue audio file path")
        audio_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        audio_entry.insert(0, node.get("dialogueAudio", ""))
        audio_entry.bind("<KeyRelease>", lambda e: self.update_node_field(act_idx, scene_idx, node_idx, "dialogueAudio", audio_entry.get()))
        
        ctk.CTkButton(
            audio_frame,
            text="Browse",
            command=lambda: self.browse_file_for_entry(audio_entry, act_idx, scene_idx, node_idx, "dialogueAudio"),
            width=80
        ).pack(side="left")
        
        text_box = ctk.CTkTextbox(parent, height=60)
        text_box.pack(fill="x", pady=2)
        
        # Add placeholder text if empty
        current_text = node.get("dialogueText", "")
        if current_text:
            text_box.insert("1.0", current_text)
        else:
            text_box.insert("1.0", "Dialogue text here...")
            text_box.configure(text_color="gray")
        
        def on_focus_in(event):
            if text_box.get("1.0", "end-1c") == "Dialogue text here...":
                text_box.delete("1.0", "end")
                text_box.configure(text_color="white")
        
        def on_focus_out(event):
            if not text_box.get("1.0", "end-1c").strip():
                text_box.insert("1.0", "Dialogue text here...")
                text_box.configure(text_color="gray")
        
        def on_key_release(event):
            text = text_box.get("1.0", "end-1c")
            if text != "Dialogue text here...":
                self.update_node_field(act_idx, scene_idx, node_idx, "dialogueText", text)
        
        text_box.bind("<FocusIn>", on_focus_in)
        text_box.bind("<FocusOut>", on_focus_out)
        text_box.bind("<KeyRelease>", on_key_release)
    
    def create_choice_widget(self, parent, act_idx: int, scene_idx: int, node_idx: int, choice_idx: int, choice: Dict):
        choice_frame = ctk.CTkFrame(parent)
        choice_frame.pack(fill="x", pady=2)
        
        button_entry = ctk.CTkEntry(choice_frame, placeholder_text="Button", width=80)
        button_entry.pack(side="left", padx=5)
        button_entry.insert(0, choice.get("button", ""))
        button_entry.bind("<KeyRelease>", lambda e: self.update_choice_field(act_idx, scene_idx, node_idx, choice_idx, "button", button_entry.get()))
        
        text_entry = ctk.CTkEntry(choice_frame, placeholder_text="Choice text")
        text_entry.pack(side="left", fill="x", expand=True, padx=5)
        text_entry.insert(0, choice.get("text", ""))
        text_entry.bind("<KeyRelease>", lambda e: self.update_choice_field(act_idx, scene_idx, node_idx, choice_idx, "text", text_entry.get()))
        
        target_entry = ctk.CTkEntry(choice_frame, placeholder_text="Target node ID", width=200)
        target_entry.pack(side="left", padx=5)
        target_entry.insert(0, choice.get("targetNodeId", ""))
        target_entry.bind("<KeyRelease>", lambda e: self.update_choice_field(act_idx, scene_idx, node_idx, choice_idx, "targetNodeId", target_entry.get()))
        
        ctk.CTkButton(
            choice_frame,
            text="X",
            command=lambda: self.delete_choice(act_idx, scene_idx, node_idx, choice_idx),
            width=40,
            fg_color="red"
        ).pack(side="left", padx=5)
    
    # Data manipulation methods
    def add_act(self):
        act_id = f"act_{len(self.project['acts'])}"
        self.project["acts"].append({
            "id": act_id,
            "name": f"Act {len(self.project['acts']) + 1}",
            "scenes": []
        })
        self.refresh_ui()
    
    def add_scene(self, act_idx: int):
        act = self.project["acts"][act_idx]
        act_id = act["id"]
        scene_id = f"{act_id}_scene_{len(act['scenes'])}"
        act["scenes"].append({
            "id": scene_id,
            "name": f"Scene {len(act['scenes']) + 1}",
            "audioTracks": [],
            "nodes": []
        })
        self.refresh_ui()
    
    def add_node(self, act_idx: int, scene_idx: int, node_type: str):
        act = self.project["acts"][act_idx]
        scene = act["scenes"][scene_idx]
        act_id = act["id"]
        scene_id = scene["id"]
        node_id = f"{scene_id}_node_{len(scene['nodes'])}"
        node = {
            "id": node_id,
            "type": node_type,
            "name": f"Node {len(scene['nodes']) + 1}",
            "choices": []
        }
        
        if node_type == "video":
            node["videoPath"] = ""
            node["dialogueText"] = ""
        else:
            node["imagePath"] = ""
            node["dialogueAudio"] = ""
            node["dialogueText"] = ""
        
        scene["nodes"].append(node)
        self.refresh_ui()
    
    def add_audio_track(self, act_idx: int, scene_idx: int):
        scene = self.project["acts"][act_idx]["scenes"][scene_idx]
        if "audioTracks" not in scene:
            scene["audioTracks"] = []
        scene["audioTracks"].append({
            "id": f"track_{len(scene['audioTracks'])}",
            "label": "BGM",
            "path": ""
        })
        self.refresh_ui()
    
    def add_choice(self, act_idx: int, scene_idx: int, node_idx: int):
        node = self.project["acts"][act_idx]["scenes"][scene_idx]["nodes"][node_idx]
        node["choices"].append({
            "id": f"choice_{len(node['choices'])}",
            "button": "",
            "text": "New Choice",
            "targetNodeId": ""
        })
        self.refresh_ui()
    
    def delete_act(self, act_idx: int):
        if messagebox.askyesno("Confirm", "Delete this act?"):
            del self.project["acts"][act_idx]
            self.refresh_ui()
    
    def delete_scene(self, act_idx: int, scene_idx: int):
        if messagebox.askyesno("Confirm", "Delete this scene?"):
            del self.project["acts"][act_idx]["scenes"][scene_idx]
            self.refresh_ui()
    
    def delete_node(self, act_idx: int, scene_idx: int, node_idx: int):
        if messagebox.askyesno("Confirm", "Delete this node?"):
            del self.project["acts"][act_idx]["scenes"][scene_idx]["nodes"][node_idx]
            self.refresh_ui()
    
    def delete_audio_track(self, act_idx: int, scene_idx: int, track_idx: int):
        del self.project["acts"][act_idx]["scenes"][scene_idx]["audioTracks"][track_idx]
        self.refresh_ui()
    
    def delete_choice(self, act_idx: int, scene_idx: int, node_idx: int, choice_idx: int):
        del self.project["acts"][act_idx]["scenes"][scene_idx]["nodes"][node_idx]["choices"][choice_idx]
        self.refresh_ui()
    
    def update_act_name(self, act_idx: int, value: str):
        self.project["acts"][act_idx]["name"] = value
    
    def update_scene_name(self, act_idx: int, scene_idx: int, value: str):
        self.project["acts"][act_idx]["scenes"][scene_idx]["name"] = value
    
    def update_node_name(self, act_idx: int, scene_idx: int, node_idx: int, value: str):
        self.project["acts"][act_idx]["scenes"][scene_idx]["nodes"][node_idx]["name"] = value
    
    def update_node_field(self, act_idx: int, scene_idx: int, node_idx: int, field: str, value: str):
        self.project["acts"][act_idx]["scenes"][scene_idx]["nodes"][node_idx][field] = value
    
    def update_audio_track(self, act_idx: int, scene_idx: int, track_idx: int, field: str, value: str):
        self.project["acts"][act_idx]["scenes"][scene_idx]["audioTracks"][track_idx][field] = value
    
    def update_choice_field(self, act_idx: int, scene_idx: int, node_idx: int, choice_idx: int, field: str, value: str):
        self.project["acts"][act_idx]["scenes"][scene_idx]["nodes"][node_idx]["choices"][choice_idx][field] = value
    
    def browse_file(self, entry_widget):
        filename = filedialog.askopenfilename()
        if filename:
            entry_widget.delete(0, "end")
            entry_widget.insert(0, filename)
    
    def browse_file_for_entry(self, entry_widget, act_idx: int, scene_idx: int, node_idx: int, field: str):
        filename = filedialog.askopenfilename()
        if filename:
            entry_widget.delete(0, "end")
            entry_widget.insert(0, filename)
            self.update_node_field(act_idx, scene_idx, node_idx, field, filename)
    
    def export_project(self):
        self.project["name"] = self.project_name.get()
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.project, f, indent=2)
            messagebox.showinfo("Success", "Project exported successfully!")
    
    def import_project(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.project = json.load(f)
                self.project_name.delete(0, "end")
                self.project_name.insert(0, self.project["name"])
                self.refresh_ui()
                messagebox.showinfo("Success", "Project imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = NeonAeonManager()
    app.run()