from pydantic import BaseModel
import uuid

"Request fields: client_id, redirect_uri, response_type, code_challenge, code_challenge_method, state (optional), email, password."


class CreateAuthorize(BaseModel):
    client_id:uuid.UUID
    redirect
