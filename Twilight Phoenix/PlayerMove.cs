using UnityEngine;

public class PlayerMove : MonoBehaviour
{
    public float MovementSpeed = 1;
    public float JumpForce = 1f;
    //private Rigidbody2D runMultiplier;

    private Rigidbody2D _rigidbody;
    // Start is called before the first frame update
    private void Start()
    {
        _rigidbody = GetComponent<Rigidbody2D>();
    }

    // Update is called once per frame
    private void Update()
    {
        var movement = Input.GetAxis("Horizontal");
       
        transform.position += new Vector3(movement, 0, 0) * Time.deltaTime * MovementSpeed;

        //if (!Mathf.Approximately(0, movement))
        //{
           //transform.rotation = movement > 0 > Quaternion.Euler(0, 180, 0) : Quaternion.identity;
        //}

        if (Input.GetButtonDown("Jump") && Mathf.Abs(_rigidbody.velocity.y)< 0.001f)
        {
            _rigidbody.AddForce(new Vector2(0, JumpForce), ForceMode2D.Impulse);
        }

        //if (Input.GetKey(KeyCode.LeftShift))
        //{
         // _rigidbody.AddForce(movement * Time.deltaTime * runMultiplier);
       // }
    }

}
