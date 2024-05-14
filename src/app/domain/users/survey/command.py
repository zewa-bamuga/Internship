#
#
# class SurveyCategoryUserAddCommand:
#     def __init__(
#         self,
#         user_create_command: UserResponseCreateCommand,
#     ) -> None:
#         self.user_create_command = user_create_command
#
#     async def __call__(self, payload: UserCredentials) -> UserDetails:
#         return await self.user_create_command(
#             UserCreate(
#                 username=payload.username,
#                 email=payload.email,
#                 avatar_attachment_id=None,
#                 permissions=set(),
#             )
#         )