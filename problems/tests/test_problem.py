from json import dumps
import pytest
from httpx import AsyncClient

from auth.utils import encode_jwt
from enums import DifficultyLevel
from problems import crud
from problems.schemas import ProblemCreate


class TestProblem:
    @pytest.mark.anyio
    @pytest.mark.parametrize(
        "name, description, difficulty_level, answer, explanation, theme_id, author_id, status_code",
        [
            (
                "problem_1",
                "Well, find this number",
                DifficultyLevel.EASY,
                "10.2",
                "Do it this way",
                1,
                1,
                403
            ),
            (
                "problem_3",
                "Well, find this number",
                DifficultyLevel.HARD,
                "10.2",
                "Do it this way",
                1,
                None,
                401
            ),
            (
                "problem_4",
                "Well, find this number",
                DifficultyLevel.EASY,
                "10.2",
                "Do it this way",
                "real",
                2,
                200
            )
        ]
    )
    async def test_create_problem(
        self,
        client: AsyncClient,
        name: str,
        description: str,
        difficulty_level: DifficultyLevel,
        answer: str,
        explanation: str,
        theme_id: int | None | str,
        author_id: int | None,
        status_code: int,
        session,
    ):
        headers = {}
        if author_id is not None:
            token = encode_jwt(payload={"sub": author_id})
            headers = {"Authorization": f"Bearer {token}"}
        if theme_id == "real":
            theme = await crud.get_theme_by_name(db=session, name="Mechanics")
            theme_id = theme.id
        json = {
            "name": name,
            "description": description,
            "difficulty_level": difficulty_level.value,
            "answer": answer,
            "explanation": explanation,
            "theme_id": theme_id
        }
        response = await client.post("/problems/", json=json, headers=headers)
        assert response.status_code == status_code

    @pytest.mark.anyio
    async def test_read_problems(self, client: AsyncClient):
        response = await client.get("/problems/")
        assert response.status_code == 200
        assert len(response.json()) == 1

    @pytest.mark.anyio
    @pytest.mark.parametrize("problem_id, status_code", [("real", 200), (-3, 404)])
    async def test_read_one_problem(
        self, client: AsyncClient, problem_id: str | int, status_code: int, session
    ):
        problems = []
        if problem_id == "real":
            problems = await crud.get_all_problems(db=session)
            problem_id = problems[0].id
        response = await client.get(f"/problems/{problem_id}/")
        assert response.status_code == status_code
        if problem_id == "real":
            assert response.json().get("name") == problems[0].name
