package validator

import (
	"fmt"
	"net/mail"

	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/pb"
)

// var (
// 	isValidUsername = regexp.MustCompile(`^[a-z0-9_]+$`).MatchString
// )

func ValidateString(value string, minLength int, maxLength int) error {
	n := len(value)
	if n < minLength || n > maxLength {
		return fmt.Errorf("must contain from %d-%d characters", minLength, maxLength)
	}
	return nil
}

func ValidateUsername(value string) error {
	if err := ValidateString(value, 3, 100); err != nil {
		return err
	}
	// if !isValidUsername(value) {
	// 	return fmt.Errorf("must contain only lowercase letters, digits, or underscore")
	// }
	return nil
}

func ValidatePassword(value string) error {
	return ValidateString(value, 6, 100)
}

func ValidateEmail(value string) error {
	if err := ValidateString(value, 3, 200); err != nil {
		return err
	}
	if _, err := mail.ParseAddress(value); err != nil {
		return fmt.Errorf("is not a valid email address")
	}
	return nil
}

func ValidateRegisterRequest(req *pb.RegisterRequest) error {
	if err := ValidateUsername(req.GetUsername()); err != nil {
		return err
	}

	if err := ValidateEmail(req.GetEmail()); err != nil {
		return err
	}

	if err := ValidatePassword(req.GetPassword()); err != nil {
		return err
	}

	return nil
}

func ValidateLoginRequest(req *pb.LoginRequest) error {

	if err := ValidateEmail(req.GetEmail()); err != nil {
		return err
	}

	if err := ValidatePassword(req.GetPassword()); err != nil {
		return err
	}

	return nil
}

func ValidateRenewTokenRequest(req *pb.RenewTokenRequest) error {

	if err := ValidateString(req.GetRefreshToken(), 3, 2000); err != nil {
		return err
	}

	return nil
}
