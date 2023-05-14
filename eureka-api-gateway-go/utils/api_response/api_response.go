package api_response

import "github.com/gin-gonic/gin"

func BaseSuccessResponse(successMessage string) gin.H {
	return gin.H{
		"status":  "success",
		"message": successMessage,
	}
}

func BaseSuccessResponseWithData(successMessage string, data interface{}) gin.H {
	return gin.H{
		"status":  "success",
		"message": successMessage,
		"data":    data,
	}
}

func BaseErrorResponse(errMessage string) gin.H {
	return gin.H{
		"status":  "failed",
		"message": errMessage,
	}
}
