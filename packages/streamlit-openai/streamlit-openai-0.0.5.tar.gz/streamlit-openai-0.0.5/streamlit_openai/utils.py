import streamlit as st
import os, tempfile
from pathlib import Path
from typing import Optional, List, Union, Callable, Dict, Any
from streamlit.runtime.uploaded_file_manager import UploadedFile

class Block():
    """
    Represents a single unit of content in a chat interface, such as text, code, or an image.

    A `Block` is used to structure and render different types of messages in the chat UI. 
    It encapsulates the content and the category (type) of that content, and includes 
    logic to render it appropriately in Streamlit.

    Attributes:
        category (str): The type of content ('text', 'code', or 'image').
        content (str or bytes): The actual content of the block, which may be a string or bytes (for images).
    """
    def __init__(
            self,
            category: str,
            content: Optional[Union[str, bytes]] = None
    ) -> None:
        self.category = category
        self.content = content

        if self.content is None:
            self.content = ""
        else:
            self.content = content

    def __repr__(self) -> None:
        if self.category == "text" or self.category == "code":
            content = self.content
            if len(content) > 50:
                content = content[:30] + "..."
        elif self.category == "image":
            content = "Bytes"
        return f"Block('category={self.category}', content='{content}')"

    def iscategory(self, category) -> bool:
        """Checks if the block belongs to the specified category."""
        return self.category == category

    def write(self) -> None:
        """Renders the block's content to the Streamlit interface."""
        if self.category == "text":
            st.markdown(self.content)
        elif self.category == "code":
            st.code(self.content)
        elif self.category == "image":
            st.image(self.content)

class Container():
    """
    Represents a single message container in a Streamlit chat interface, 
    managing role-based message blocks and real-time updates.

    This class holds a sequence of message blocks (e.g., text, code, image) 
    associated with a role (e.g., "user", "assistant"), and handles updating, 
    rendering, and streaming content to the UI.

    Attributes:
        delta_generator: A Streamlit placeholder used for dynamic content updates.
        role (str): The role associated with this message (e.g., "user" or "assistant").
        blocks (list): A list of Block instances representing message segments.
    """
    def __init__(
            self,
            role: str,
            blocks: Optional[List[Block]] = None,
    ) -> None:
        self.delta_generator = st.empty()
        self.role = role
        self.blocks = blocks

    def __repr__(self) -> None:
        return f"Container(role='{self.role}', blocks={self.blocks})"

    @property
    def empty(self) -> bool:
        """Returns True if the container has no blocks."""
        return self.blocks is None

    @property
    def last_block(self) -> Optional[Block]:
        """Returns the last block in the container or None if empty."""
        return None if self.empty else self.blocks[-1]

    def update(self, category, content) -> None:
        """Updates the container with new content, appending or extending existing blocks."""
        if self.empty:
            self.blocks = [Block(category, content)]
        elif self.last_block.iscategory(category):
            self.last_block.content += content
        else:
            self.blocks.append(Block(category, content))

    def write(self) -> None:
        """Renders the container's content in the Streamlit chat interface."""
        if self.empty:
            pass
        else:
            with st.chat_message(self.role):
                for block in self.blocks:
                    block.write()

    def update_and_stream(self, category, content) -> None:
        """Updates the container and streams the update live to the UI."""
        self.update(category, content)
        self.stream()

    def stream(self) -> None:
        """Renders the container content using Streamlit's delta generator."""
        with self.delta_generator:
            self.write()

class TrackedFile():
    """
    A class to represent a file that is tracked and managed within the OpenAI and Streamlit integration.

    Attributes:
        uploaded_file (UploadedFile): The UploadedFile object created by Streamlit.
        openai_file (File): The File object created by OpenAI.
        removed (bool): A flag indicating whether the file has been removed.
    """
    def __init__(
            self,
            uploaded_file: UploadedFile
    ) -> None:
        self.uploaded_file = uploaded_file
        self.openai_file = None
        self.removed = False

    def __repr__(self) -> None:
        return f"TrackedFile(uploaded_file='{self.uploaded_file.name}', deleted={self.removed})"

    def to_openai(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            file_path = os.path.join(t, self.uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(self.uploaded_file.getvalue())
            self.openai_file = st.session_state.chat.client.files.create(file=Path(file_path), purpose="assistants")
            st.session_state.chat.client.beta.threads.messages.create(
                thread_id=st.session_state.chat.thread.id,
                role="user",    
                content=f"File uploaded: {self.uploaded_file.name}",
                attachments=[{"file_id": self.openai_file.id, "tools": [{"type": "file_search"}]}]
            )

    def remove(self) -> None:
        response = st.session_state.chat.client.files.delete(self.openai_file.id)
        if not response.deleted:
            raise ValueError("File could not be deleted from OpenAI: ", self.uploaded_file.name)
        st.session_state.chat.client.beta.threads.messages.create(
            thread_id=st.session_state.chat.thread.id,
            role="user",
            content=f"File removed: {self.uploaded_file.name}",
        )
        self.removed = True

class CustomFunction():
    """
    Represents a user-defined function and its corresponding OpenAI function 
    definition.

    This class wraps a callable Python function with metadata in the format 
    expected by OpenAI's function-calling tools.

    Attributes:
        definition (dict): The OpenAI-compatible function schema/definition.
        function (Callable): The actual Python function to be executed when invoked.
    """
    def __init__(
            self,
            definition: Dict[str, Any],
            function: Callable,
    ) -> None:
        self.definition = definition
        self.function = function

    def __repr__(self) -> None:
        return f"CustomFunction(definition='{self.definition}')"