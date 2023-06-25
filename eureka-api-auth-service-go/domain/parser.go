package domain

import (
	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/pb"
	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/utils/methods"
)

func ParseDomainFromReq(request interface{}) interface{} {

	switch r := request.(type) {

	case *pb.RegisterRequest:

		return User{
			ID:        GenerateUserID(),
			Name:      r.GetUsername(),
			Email:     r.GetEmail(),
			Password:  r.GetPassword(),
			CreatedAt: methods.GetCurrentTimestamp(),
		}

	default:

		return nil

	}
}
