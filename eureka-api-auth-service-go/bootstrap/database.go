package bootstrap

import (
	"log"
	"sync"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
)

const (
	usersTableName    = "eureka_api_auth_service_go__users_table"
	sessionsTableName = "eureka_api_auth_service_go__sessions_table"
)

type Database struct {
	Client            *dynamodb.DynamoDB
	UsersTableName    string
	SessionsTableName string
}

type DatabaseTable struct {
	Name string
}

type databaseTableCreateFields struct {
	Name                   string
	AttributeDefinition    []*dynamodb.AttributeDefinition
	KeySchema              []*dynamodb.KeySchemaElement
	GlobalSecondaryIndexes []*dynamodb.GlobalSecondaryIndex
}

func NewDynamoDbDatabase(env *Env) *Database {

	var sess *session.Session

	if env.AppEnv == "PRODUCTION" {

		sess = session.Must(session.NewSessionWithOptions(session.Options{
			SharedConfigState: session.SharedConfigEnable,
		}))

	} else {

		sess = session.Must(session.NewSession(&aws.Config{
			Endpoint: aws.String("http://localhost:8000"),
			Region:   aws.String("us-west-2"),
		}))

	}

	databaseTablesCreateFields := []databaseTableCreateFields{

		{
			Name: usersTableName,
			AttributeDefinition: []*dynamodb.AttributeDefinition{
				{
					AttributeName: aws.String("id"),
					AttributeType: aws.String("S"),
				},
				{
					AttributeName: aws.String("email"),
					AttributeType: aws.String("S"),
				},
			},
			KeySchema: []*dynamodb.KeySchemaElement{
				{
					AttributeName: aws.String("id"),
					KeyType:       aws.String("HASH"),
				},
			},
			GlobalSecondaryIndexes: []*dynamodb.GlobalSecondaryIndex{
				{
					IndexName: aws.String("EmailIndex"),
					KeySchema: []*dynamodb.KeySchemaElement{
						{
							AttributeName: aws.String("email"),
							KeyType:       aws.String("HASH"),
						},
					},
					Projection: &dynamodb.Projection{
						ProjectionType: aws.String("ALL"),
					},
					ProvisionedThroughput: &dynamodb.ProvisionedThroughput{
						ReadCapacityUnits:  aws.Int64(5),
						WriteCapacityUnits: aws.Int64(5),
					},
				},
			},
		},

		{
			Name: sessionsTableName,
			AttributeDefinition: []*dynamodb.AttributeDefinition{
				{
					AttributeName: aws.String("id"),
					AttributeType: aws.String("S"),
				},
			},
			KeySchema: []*dynamodb.KeySchemaElement{
				{
					AttributeName: aws.String("id"),
					KeyType:       aws.String("HASH"),
				},
			},
			GlobalSecondaryIndexes: []*dynamodb.GlobalSecondaryIndex{},
		},
	}

	dbClient := dynamodb.New(sess)

	var wg sync.WaitGroup

	errCh := make(chan error)

	// Launch goroutines to create tables concurrently
	for _, databaseTableCreateFields := range databaseTablesCreateFields {
		wg.Add(1)
		go createTableIfNotExists(dbClient, databaseTableCreateFields.Name, databaseTableCreateFields.AttributeDefinition, databaseTableCreateFields.KeySchema, databaseTableCreateFields.GlobalSecondaryIndexes, &wg, errCh)
	}

	go func() {
		wg.Wait()
		close(errCh)
	}()

	for err := range errCh {
		if err != nil {
			log.Fatal("Error creating table:", err)
		}
	}

	log.Println("Table creation completed!")

	return &Database{
		Client:            dbClient,
		UsersTableName:    usersTableName,
		SessionsTableName: sessionsTableName,
	}
}

func createTableIfNotExists(client *dynamodb.DynamoDB, tableName string, attributeDefinitions []*dynamodb.AttributeDefinition, keySchema []*dynamodb.KeySchemaElement, GlobalSecondaryIndex []*dynamodb.GlobalSecondaryIndex, wg *sync.WaitGroup, errCh chan<- error) {
	defer wg.Done()

	// Check if the table exists
	_, err := client.DescribeTable(&dynamodb.DescribeTableInput{
		TableName: aws.String(tableName),
	})

	// If the table doesn't exist, create it
	if err != nil {
		// Create the table definition
		table := DatabaseTable{Name: tableName}
		_, err := dynamodbattribute.MarshalMap(table)
		if err != nil {
			errCh <- err
			return
		}

		log.Printf("Creating table: %s\n", tableName)

		// Create the table input
		input := &dynamodb.CreateTableInput{
			TableName:            aws.String(tableName),
			AttributeDefinitions: attributeDefinitions,
			KeySchema:            keySchema,
			ProvisionedThroughput: &dynamodb.ProvisionedThroughput{
				ReadCapacityUnits:  aws.Int64(5),
				WriteCapacityUnits: aws.Int64(5),
			},
		}

		// Add Global Secondary Index if it's not empty
		if len(GlobalSecondaryIndex) > 0 {
			input.GlobalSecondaryIndexes = GlobalSecondaryIndex
		}

		// Create the table
		_, err = client.CreateTable(input)
		if err != nil {
			errCh <- err
			return
		}

		log.Printf("Created table: %s\n", tableName)
	}
}
