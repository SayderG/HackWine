from database.models.users import Users, UserLogin, UserReg
from database.repositories.BaseRepository import BaseRepository
from fastapi import HTTPException
from sqlalchemy import select


class UsersRepository(BaseRepository):
    model = Users

    async def login(self, login: UserLogin):
        query = await self.session.execute(select(self.model).where(self.model.login == login.login))
        user = query.scalars().first()
        if user:
            if self.model.verify_password(login.password, user.password):
                return user
            else:
                raise HTTPException(status_code=401, detail="invalid password")
        raise HTTPException(status_code=404, detail="user not found")

    async def registration(self, regData: UserReg):
        user = Users(username=regData.username, login=regData.login, password=Users.hash_password(regData.password))
        self.session.add(user)
        await self.session.commit()
        return user

