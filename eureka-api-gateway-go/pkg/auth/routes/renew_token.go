package routes

import (
	"context"
	"net/http"

	"github.com/Ayobami-00/Eureka/eureka-api-gateway-go/pkg/auth/pb"
	"github.com/Ayobami-00/Eureka/eureka-api-gateway-go/utils/api_response"
	"github.com/gin-gonic/gin"
)

type RenewTokenRequestBody struct {
	RefreshToken string `json:"refresh_token"`
}

func RenewToken(ctx *gin.Context, c pb.AuthServiceClient) {

	reqBody := RenewTokenRequestBody{}

	if err := ctx.BindJSON(&reqBody); err != nil {
		ctx.JSON(http.StatusBadRequest, api_response.BaseErrorResponse(err.Error()))
		return
	}

	res, _ := c.RenewToken(context.Background(), &pb.RenewTokenRequest{
		RefreshToken: reqBody.RefreshToken,
	})

	api_response.Respond(ctx, res)

}
